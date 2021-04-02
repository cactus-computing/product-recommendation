import json
from woocommerce import API
from datetime import datetime
import os
import logging
import time
from tqdm import tqdm
import glob
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from products.models import OrderAttributes, ProductAttributes
from store.models import Store

with open('./scripts/wc/wc-keys.json') as f:
  keys = json.load(f) 
def run(*args):
    COMPANY = args[0]
    CONSUMER_KEY = keys[COMPANY]["CONSUMER_KEY"]
    CONSUMER_SECRET = keys[COMPANY]["CONSUMER_SECRET"]
    company = Store.objects.get(company=COMPANY)
    #last_date = OrderAttributes.objects.filter(company=company).latest("record_created_at")
    #last_date = last_date.record_created_at
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
    endpoint="orders"
    logger.info("Getting products")
    for e in tqdm(range(100)):
        params = {
                'per_page': 50,
                'page': e+1,
                'status':['completed'],#, 'pending payment', 'processing'],
                #'after':last_date,
                'orderby':'date',
                'order':'asc',
            }
        resp = wcapi.get(endpoint, params=params).json()
        if resp == []:
            break
        else:
            for item in resp:
                for prod in item['line_items']:
                    try:
                        product_code = ProductAttributes.objects.get(product_code=prod['product_id'], company=company)
                    except ProductAttributes.DoesNotExist as f:
                        logger.error(f)
                        continue
                    try:
                        OrderAttributes.objects.update_or_create(
                            user=item['customer_id'],
                            product=product_code,
                            product_qty=prod['quantity'],
                            bill=item['id'],
                            product_name=prod['name'],
                            company=company,
                            record_created_at=item['date_created']
                            )
                    except IntegrityError as f:
                        logger.error(f)
                        continue
        time.sleep(2)