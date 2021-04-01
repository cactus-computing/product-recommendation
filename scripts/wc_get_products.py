import json
from woocommerce import API
from datetime import datetime
from .wc.storage import  upload_blob_to_default_bucket
import os
import logging
import time
from tqdm import tqdm
import glob
from products.models import ProductAttributes
from store.models import Store

with open('./scripts/wc/wc-keys.json') as f:
  keys = json.load(f) 
def run(*args):
    COMPANY = args[0]
    CONSUMER_KEY = keys[COMPANY]["CONSUMER_KEY"]
    CONSUMER_SECRET = keys[COMPANY]["CONSUMER_SECRET"]
    API_URL = keys[COMPANY]["API_URL"]
    DATE = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
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
            logging.FileHandler(f'./scripts/wc/logs/{COMPANY}_{DATE}.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    endpoint="products"
    logger.info("Getting products")
    company = Store.objects.get(company=COMPANY)
    products = []
    for e in tqdm(range(100)):
        params = {
                'per_page': 50,
                'page': e+1,
                'status':['any'],
                'order':'asc',
            }
        resp = wcapi.get(endpoint, params=params).json()
        if resp == []:
            break
        else:
            for item in resp:
                sku = item['sku']
                if sku == '':
                    sku = item['id']
                if item['status'] == "publish":
                    ProductAttributes.objects.update_or_create(
                        product_code=item['id'],
                        sku=sku,
                        company=company,
                        defaults={
                            'name': item['name'],
                            'permalink': item['permalink'],
                            'img_url': item['images'][0]['src'] if item['images'] != [] else "https://www.quema.cl/wp-content/uploads/woocommerce-placeholder.png",
                            'stock_quantity': False if item['stock_status'] == "outofstock" else True,
                            'status': item['status'],
                            'price': item['price'] if item['price'] else None
                        }
                    )
        time.sleep(2)