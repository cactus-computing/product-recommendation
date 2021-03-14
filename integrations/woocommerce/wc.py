import json
import oauth2 as oauth
from woocommerce import API
import sys
from datetime import datetime
from django.utils import timezone
from storage import  upload_blob_to_default_bucket
import os

with open('./integrations/woocommerce/wc-keys.json') as f:
  keys = json.load(f) 

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

def get_orders(wcapi=wcapi):
    endpoint = "orders"
    params = {
        'per_page': 100,
        'page': 1,
    }
    resp = wcapi.get(endpoint, params=params).json()
    filename = './integrations/woocommerce/orders.json'
    with open(filename, 'w+') as f:
        f.write(json.dumps(resp))
    blob_name = f"{COMPANY}/{endpoint}_{DATE}.json"
    upload_blob_to_default_bucket(filename,blob_name)
    os.remove(filename)

def get_products(wcapi=wcapi):
    endpoint = "products"
    params = {
        'per_page': 100,
        'page': 1,
    }
    resp = wcapi.get(endpoint, params=params).json()
    filename = './integrations/woocommerce/products.json'
    with open(filename, 'w+') as f:
        f.write(json.dumps(resp))
    blob_name = f"{COMPANY}/{endpoint}_{DATE}.json"
    upload_blob_to_default_bucket(filename,blob_name)
    os.remove(filename)

def upload_upsell(wcapi=wcapi):
    up_sell = ["18"]
    coss_sell = ["12"]
    data = {
        "upsell_ids": up_sell,
        "cross_sell_ids": coss_sell
    }
    id_producto = "14"
    print(wcapi.put(f"products/{id_producto}", data).json())


if __name__ == "__main__":
    if METHOD == "get_data":
        get_orders()
        get_products()
    elif METHOD == "post_data":
        upload_upsell()