import json
import oauth2 as oauth
from woocommerce import API
import sys
from datetime import datetime
from storage import  upload_blob_to_default_bucket
import os
import logging
import time
from tqdm import tqdm
import glob

with open('./integrations/woocommerce/wc-keys.json') as f:
  keys = json.load(f) 
  
COMPANY = sys.argv[1]
METHOD = sys.argv[2]
CONSUMER_KEY = keys[COMPANY]["CONSUMER_KEY"]
CONSUMER_SECRET = keys[COMPANY]["CONSUMER_SECRET"]
API_URL = keys[COMPANY]["API_URL"]
DATE = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
CROSS_SELL = sorted(glob.glob(f"./integrations/woocommerce/{COMPANY}/cross_selling_run_*.json"), reverse=True)[0]
UP_SELL = sorted(glob.glob(f"./integrations/woocommerce/{COMPANY}/up_selling_run_*.json"), reverse=True)[0]
wcapi = API(
    url=API_URL,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    version="wc/v3",
    query_string_auth=True
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f'./integrations/woocommerce/logs/{COMPANY}_{DATE}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def get_orders_prod(wcapi=wcapi, endpoints=["orders", "products"]):
    logger.info("Getting orders and products")
    for endpoint in endpoints:
        logger.info(f"Getting {endpoint}")
        json_file = []
        for e in tqdm(range(100)):
            params = {
                    'per_page': 50,
                    'page': e+1,
                    'status':['any'],
                    'order':'asc',
                }
            if endpoint == "orders":
                pass
                #params['after'] = "" #Limit response to resources published after a given ISO8601 compliant date.
            else:
                pass
                #params['exclude'] = "" #Ensure result set excludes specific IDs.
            resp = wcapi.get(endpoint, params=params).json()
            logger.info(resp)
            if resp == []:
                break
            else:
                for item in resp:
                    json_file.append(item)
            time.sleep(1)
        blob_name = f"{COMPANY}/{endpoint}.json"
        upload_blob_to_default_bucket(json_file,blob_name)
        if COMPANY == "cactus":
            with open(F'./integrations/woocommerce/test_cactus/{endpoint}.json', 'w+') as f:
                json.dump(json_file, f)

def upload_upsell(wcapi=wcapi):
    logger.info("starting")
    with open(F'{CROSS_SELL}', 'r+') as f:
        logger.info(CROSS_SELL)
        cross_sell = json.load(f)
    with open(F'{UP_SELL}', 'r+') as f:
        logger.info(UP_SELL)
        up_sell = json.load(f)
    for item in tqdm(cross_sell['data']):
        logger.info(item)
        id_product = item['ORIGINAL_PRODUCT_CODE']
        cosssell = []
        for related_item in item['RECOMMENDATIONS']:
            cosssell.append(related_item['RECOMMENDED_PRODUCT_ID'])
        upsell = []
        for item in up_sell['data']:
            if item['ORIGINAL_PRODUCT_CODE'] == id_product:
                for upsell_item in item['RECOMMENDATIONS']:
                    upsell.append(upsell_item['RECOMMENDED_PRODUCT_ID'])
        data = {
            "upsell_ids": upsell,
            "cross_sell_ids": cosssell
        }
        logger.info(wcapi.put(f"products/{id_product}", data).json())


if __name__ == "__main__":
    if METHOD == "get_data":
        get_orders_prod()
    elif METHOD == "post_data":
        upload_upsell()

    