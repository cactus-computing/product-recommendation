import json
import oauth2 as oauth
from woocommerce import API
import sys
from datetime import datetime
from django.utils import timezone
from storage import  upload_blob_to_default_bucket
import os
import logging

with open('./integrations/woocommerce/wc-keys.json') as f:
  keys = json.load(f) 

logger = logging.Logger(__name__)

COMPANY = sys.argv[1]
METHOD = sys.argv[2]
CONSUMER_KEY = keys[COMPANY]["CONSUMER_KEY"]
CONSUMER_SECRET = keys[COMPANY]["CONSUMER_SECRET"]
API_URL = keys[COMPANY]["API_URL"]
DATE = datetime.today().strftime('%Y-%m-%d %H-%m-%s')
wcapi = API(
    url=API_URL,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    version="wc/v3"
)

def get_orders_prod(wcapi=wcapi):
    logger.info("Getting orders and products")
    endpoints = ["orders", "products"]
    for endpoint in endpoints:
        logger.info(f"Getting {endpoint}")
        pages = []
        for e in range(10000):
            params = {
                    'per_page': 100,
                    'page': e+1,
                    #'status':['completed'],
                    'order':'asc',
                }
            if endpoint == "orders":
                pass
                #params['after'] = "" #Limit response to resources published after a given ISO8601 compliant date.
            else:
                pass
                #params['exclude'] = "" #Ensure result set excludes specific IDs.
            resp = wcapi.get(endpoint, params=params).json()
            if resp == []:
                break
            else:
                for page in resp:
                    pages.append(page)
        filename = f'./integrations/woocommerce/{endpoint}.json'
        with open(filename, 'w+') as f:
            f.write(json.dumps(pages))
        blob_name = f"{COMPANY}/{endpoint}_{DATE}.json"
        logger.info(f"File {blob_name} saved in GCS")
        upload_blob_to_default_bucket(filename,blob_name)
        #os.remove(filename)

def upload_upsell(wcapi=wcapi):

    id_producto = "14"
    up_sell = ["18"]
    coss_sell = ["12"]
    data = {
        "upsell_ids": up_sell,
        "cross_sell_ids": coss_sell
    }
    
    print(wcapi.put(f"products/{id_producto}", data).json())


if __name__ == "__main__":
    if METHOD == "get_data":
        get_orders_prod()
    elif METHOD == "post_data":
        upload_upsell()