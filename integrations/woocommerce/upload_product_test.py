import json
import oauth2 as oauth
from woocommerce import API
import sys
from datetime import datetime
from storage import  upload_blob_to_default_bucket
import os
import logging
import time

with open('./integrations/woocommerce/wc-keys.json') as f:
  keys = json.load(f) 

logger = logging.Logger(__name__)

COMPANY = sys.argv[1]
COMPANY2 = sys.argv[2]
CONSUMER_KEY = keys[COMPANY]["CONSUMER_KEY"]
CONSUMER_SECRET = keys[COMPANY]["CONSUMER_SECRET"]
API_URL = keys[COMPANY]["API_URL"]
DATE = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
wcapi = API(
    url=API_URL,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    version="wc/v3"
)

def create_prod(wcapi=wcapi):
    logger.info("Getting orders and products")
    endpoint = "products/batch"
    logger.info(f"Getting {endpoint}")
    with open(f'./integrations/woocommerce/{COMPANY2}/makers_product.json', 'r+') as f:
        json_file = json.load(f)
    with open(f'./integrations/woocommerce/{COMPANY2}/products_cactus.json', 'r+') as f:
        productos_arriba = json.load(f)
    
    skus = []
    for pord in productos_arriba:
        skus.append(pord["sku"])
    print(skus)
    new_prod = []
    
    for e, product in enumerate(json_file):
        if product['id'] in skus:
            print(product['id'])
            data = {
                "name": product['name'],
                "type": product['type'],
                "regular_price": product['regular_price'],
                "sku": product['id'],
                "virtual": product['virtual'],
                "downloadable": product['downloadable'],
                "downloads": product['downloads'],
                "categories": product['categories'],
            }
            new_prod.append(data)
            up_prod = {
                'create':new_prod
            }
            print(f"new_prod leng = {len(new_prod)}")
            print(wcapi.post("products/batch", up_prod).json())
            new_prod = []

def upload_related_prod(wcapi=wcapi):
    empty_product = []
    with open(f'./integrations/woocommerce/{COMPANY2}/products.json', 'r+') as f:
        productos_arriba = json.load(f)
    skus2id = {}
    for prod in productos_arriba:
        skus2id[prod["sku"]] = prod["id"]
        #skus2id[prod["id"]] = prod["sku"] 
    with open(f'./integrations/woocommerce/{COMPANY2}/cross_selling_run_20210318.json', 'r+') as f:
        json_file = json.load(f)    
    with open(f'./integrations/woocommerce/{COMPANY2}/up_selling_run_20210317.json', 'r+') as f:
        upsell = json.load(f)    
    for e, item in enumerate(json_file['data']):
        try:
            id_product = skus2id[str(item['ORIGINAL_PRODUCT_CODE'])]
            print(f"origina id: {item['ORIGINAL_PRODUCT_CODE']}, cactus id: {skus2id[str(item['ORIGINAL_PRODUCT_CODE'])]}")
        except:
            print(f"{item['ORIGINAL_PRODUCT_CODE']} sku not maped")
            id_product = None
            continue
        cross_sell = []
        up_sell = []
        for related_item in item['RECOMMENDATIONS']:
            try:
                cross_sell.append(skus2id[str(related_item['RECOMMENDED_PRODUCT_ID'])])
            except:
                print(f"{related_item['RECOMMENDED_PRODUCT_ID']} related id not maped")
        for upsell_ids in upsell['data']:
            if upsell_ids['ORIGINAL_PRODUCT_CODE'] == item['ORIGINAL_PRODUCT_CODE']:
                for upsell_item in upsell_ids['RECOMMENDATIONS']:
                    try:
                        print(skus2id[str(upsell_item['RECOMMENDED_PRODUCT_ID'])])
                        up_sell.append(skus2id[str(upsell_item['RECOMMENDED_PRODUCT_ID'])])
                    except:
                        print(f"{related_item['RECOMMENDED_PRODUCT_ID']} related id not maped")
        data = {
        "upsell_ids": up_sell,
        "cross_sell_ids": cross_sell
        }
        if id_product is not None:
            resp = wcapi.put(f"products/{id_product}", data).json()
            with open(f'./integrations/woocommerce/{COMPANY2}/response.json', 'a+') as f:
                json.dump(resp, f)
        else:
            empty_product.append({
                "ID":item['ORIGINAL_PRODUCT_CODE'],
                "cross_sell":cross_sell,
                "upsell":up_sell
            })
    with open(f'./integrations/woocommerce/{COMPANY2}/empty_products.json', 'w+') as f:
        json.dump(empty_product,f)    

if __name__ == "__main__":
    upload_related_prod()
    #create_prod()
