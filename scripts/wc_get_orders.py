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

def run(*args):
    company_name = args[0]
    company = Store.objects.get(company=company_name)
    consumer_key = company.consumer_key
    consumer_secret = company.consumer_secret
    #last_date = OrderAttributes.objects.filter(company=company).latest("record_created_at")
    #last_date = last_date.record_created_at
    api_url = company.api_url
    DATE = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    wcapi = API(
        url=api_url,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
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
                            company=company
                            )
                    except IntegrityError as f:
                        logger.error(f)
                        continue
        time.sleep(2)