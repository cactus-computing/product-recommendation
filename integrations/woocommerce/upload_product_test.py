import json
from woocommerce import API
import sys
from datetime import datetime
import logging
import time
import glob
import os
from tqdm import tqdm

with open('./integrations/woocommerce/wc-keys.json') as f:
  keys = json.load(f) 


COMPANY = sys.argv[1]
METHOD = sys.argv[2]
CONSUMER_KEY = keys["cactus"]["CONSUMER_KEY"]
CONSUMER_SECRET = keys["cactus"]["CONSUMER_SECRET"]
API_URL = keys["cactus"]["API_URL"]
DATE = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
wcapi = API(
    url=API_URL,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    version="wc/v3",
    query_string_auth=True
)

CROSS_SELL = sorted(glob.glob(f"./integrations/woocommerce/{COMPANY}/cross_selling_run_*.json"), reverse=True)[0]
UP_SELL = sorted(glob.glob(f"./integrations/woocommerce/{COMPANY}/up_selling_run_*.json"), reverse=True)[0]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f'./integrations/woocommerce/logs/test_{DATE}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def create_prod(wcapi=wcapi):
    """
    Given a json file it creates products in ecommerce.cactusco.cl
    """
    logger.info("Getting orders and products")
    endpoint = "products/batch"
    logger.info(f"Getting {endpoint}")
    with open(f'./integrations/woocommerce/{COMPANY}/products.json', 'r+') as f:
        json_file = json.load(f)
    logger.info(f'Creating {len(json_file)} new products')
    new_prod = []
    for e, product in enumerate(tqdm(json_file)):
        logger.info(product['id'])
        data = {
            "name": product['name'],
            "type": product['type'],
            "regular_price": product['regular_price'],
            "sku": product['id'],
            "status": product['status'],
            "virtual": product['virtual'],
            "downloadable": product['downloadable'],
            "downloads": product['downloads'],
            "categories": product['categories'],
        }
        new_prod.append(data)
        up_prod = {
            'create':new_prod
        }
        logger.info(wcapi.post("products/batch", up_prod).json())
        new_prod = []
        time.sleep(1)

def upload_related_prod(wcapi=wcapi):
    """
    Given reltaded products files it uploads products related links
    """
    empty_product = []
    with open(f'./integrations/woocommerce/test_cactus/products.json', 'r+') as f:
        productos_arriba = json.load(f)
    skus2id = {}
    for prod in productos_arriba:
        skus2id[prod["sku"]] = prod["id"]
        #skus2id[prod["id"]] = prod["sku"] 
    with open(f'{CROSS_SELL}', 'r+') as f:
        logger.info(f'{CROSS_SELL}')
        cross = json.load(f)    
    with open(f'{UP_SELL}', 'r+') as f:
        logger.info(f'{UP_SELL}')
        upsell = json.load(f)    
    logger.info(f'Uploading {len(cross["data"])} new products')
    logger.info(cross['data'])
    for e, item in enumerate(tqdm(cross['data'])):
        try:
            id_product = skus2id[str(item['ORIGINAL_PRODUCT_CODE'])]
            logger.info(f"original id: {item['ORIGINAL_PRODUCT_CODE']}, cactus id: {skus2id[str(item['ORIGINAL_PRODUCT_CODE'])]}")
        except:
            logger.info(f"{item['ORIGINAL_PRODUCT_CODE']} sku not maped")
            id_product = None
            continue
        cross_sell = []
        up_sell = []
        for related_item in item['RECOMMENDATIONS']:
            try:
                cross_sell.append(skus2id[str(related_item['RECOMMENDED_PRODUCT_ID'])])
            except:
                logger.info(f"{related_item['RECOMMENDED_PRODUCT_ID']} related id not maped")
        for upsell_ids in upsell['data']:
            if upsell_ids['ORIGINAL_PRODUCT_CODE'] == item['ORIGINAL_PRODUCT_CODE']:
                for upsell_item in upsell_ids['RECOMMENDATIONS']:
                    try:
                        logger.info(skus2id[str(upsell_item['RECOMMENDED_PRODUCT_ID'])])
                        up_sell.append(skus2id[str(upsell_item['RECOMMENDED_PRODUCT_ID'])])
                    except:
                        logger.info(f"{related_item['RECOMMENDED_PRODUCT_ID']} related id not maped")
        data = {
        "upsell_ids": up_sell,
        "cross_sell_ids": cross_sell
        }
        if id_product is not None:
            resp = wcapi.put(f"products/{id_product}", data).json()
            with open(f'./integrations/woocommerce/{COMPANY}/response.json', 'a+') as f:
                json.dump(resp, f)
        else:
            empty_product.append({
                "ID":item['ORIGINAL_PRODUCT_CODE'],
                "cross_sell":cross_sell,
                "upsell":up_sell
            })
    with open(f'./integrations/woocommerce/{COMPANY}/empty_products.json', 'w+') as f:
        json.dump(empty_product,f)    


def delete_test_prod(wcapi=wcapi):
    """
    Given a json file it deletes products in ecommerce.cactusco.cl
    """
    endpoint = "products/batch"
    with open(f'./integrations/woocommerce/test_cactus/products.json', 'r+') as f:
        productos_arriba = json.load(f)
    logger.info(f'Deleting {len(productos_arriba)} new products')
    delete = []
    for e, pord in enumerate(tqdm(productos_arriba)):
        delete.append(pord["id"])
        if e % 10 == 0:
            data = {
                "delete": delete
            }
            logger.info(wcapi.post("products/batch", data).json())
            delete = []
            time.sleep(1)
            
if __name__ == "__main__":
    if METHOD == "related_prod":
        upload_related_prod()
    elif METHOD == "delete_prod":
        delete_test_prod()
    elif METHOD == "create_prod":    
        create_prod()
