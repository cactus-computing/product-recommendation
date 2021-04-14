import json
from woocommerce import API
from datetime import datetime
import os
import logging
import time
from tqdm import tqdm
import glob
from django.db.utils import IntegrityError
from products.models import ProductAttributes
from store.models import Store

date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(f'./scripts/wc/logs/log_{date}.log'),
            logging.StreamHandler()
        ]
    )
logger = logging.getLogger(__name__)

def run():
    company_names = ['quema', 'makerschile']
    for company_name in company_names:
        company = Store.objects.get(company=company_name)
        consumer_key = company.consumer_key
        consumer_secret = company.consumer_secret
        api_url = company.api_url
        
        wcapi = API(
            url=api_url,
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            version="wc/v3",
            query_string_auth=True
        )
        endpoint="products"
        logger.info(f"Getting products from {company_name}")
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
                        status = True
                    else:
                        status = False
                        print(item['status'])
                    if item['regular_price']:
                        price = item['regular_price']
                    elif item['price']:
                        price = item['price']
                    else:
                        price = None
                    try:
                        ProductAttributes.objects.update_or_create(
                            company=company,
                            name=item['name'],
                            permalink=item['permalink'],
                            defaults={
                                'product_code':item['id'],
                                'sku':sku,
                                'img_url': item['images'][0]['src'] if item['images'] != [] else "https://www.quema.cl/wp-content/uploads/woocommerce-placeholder.png",
                                'stock_quantity': False if item['stock_status'] == "outofstock" else True,
                                'status': status,
                                'discounted_price': item['sale_price'] if item['sale_price'] else None,
                                'price': price,
                                'product_created_at': item['date_created']
                            }
                        )
                    except IntegrityError as f:
                        logger.error(f)
                        continue
            time.sleep(2)