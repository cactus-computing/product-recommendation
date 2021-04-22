import json
from woocommerce import API
from datetime import datetime
import logging
import time
from tqdm import tqdm
from django.db.utils import IntegrityError
from products.models import ProductAttributes, OrderAttributes
from store.models import Store, Customers, Integration

date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler('./products/scripts/logs/log_.log'),
            logging.StreamHandler()
        ]
    )
logger = logging.getLogger(__name__)

def get_products(store_name):
    store = Store.objects.get(company=store_name)
    store_credentials = Integration.objects.get(store=store)
    consumer_key = store_credentials.consumer_key
    consumer_secret = store_credentials.consumer_secret
    api_url = store_credentials.api_url
    wcapi = API(
        url=api_url,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        version="wc/v3",
        query_string_auth=True
    )
    endpoint="products"
    logger.info(f"Getting products for {store_name}, woocommerce")
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
                if item['regular_price']:
                    price = item['regular_price']
                elif item['price']:
                    price = item['price']
                else:
                    price = None
                try:
                    ProductAttributes.objects.update_or_create(
                        company=store,
                        name=item['name'],
                        permalink=item['permalink'],
                        defaults={
                            'product_code':item['id'],
                            'sku':sku,
                            'img_url': item['images'][0]['src'] if item['images'] != [] else "https://www.quema.cl/wp-content/uploads/woocommerce-placeholder.png",
                            'stock_quantity': False if item['stock_status'] == "outofstock" else True,
                            'status': status,
                            'price': item['sale_price'] if item['sale_price'] else price,
                            'compare_at_price': price if item['sale_price'] else None,
                            'product_created_at': item['date_created']
                        }
                    )
                except IntegrityError as f:
                    logger.error(f)
                    continue
        time.sleep(2)


def get_customers(store_name):
    store = Store.objects.get(company=store_name)
    store_credentials = Integration.objects.get(store=store)
    consumer_key = store_credentials.consumer_key
    consumer_secret = store_credentials.consumer_secret
    api_url = store_credentials.api_url
    wcapi = API(
        url=api_url,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        version="wc/v3",
        query_string_auth=True
    )
    endpoint="customers"
    logger.info(f"Getting customers for {store_name}, woocommerce")
    for e in tqdm(range(100)):
        params = {
                'per_page': 50,
                'page': e+1,
                'status':['completed'],#, 'pending payment', 'processing'],
                #'after':last_date,
                'orderby':'registered_date',
                'order':'asc',
            }
        resp = wcapi.get(endpoint, params=params).json()
        if resp == []:
            break
        else:
            for customer in resp:
                if customer['role'] == "customer":
                    try:
                        Customers.objects.update_or_create(
                            store = store,
                            name = customer['first_name'],
                            last_name = customer['last_name'],
                            email = customer['email'],
                            defaults={
                                'customers_code': customer['id'],
                                'accepts_marketing': True,
                            }
                            )
                    except IntegrityError as f:
                        logger.error(f)
                        continue
        time.sleep(2)

def get_orders(store_name):
    store = Store.objects.get(company=store_name)
    store_credentials = Integration.objects.get(store=store)
    consumer_key = store_credentials.consumer_key
    consumer_secret = store_credentials.consumer_secret
    api_url = store_credentials.api_url
    wcapi = API(
        url=api_url,
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        version="wc/v3",
        query_string_auth=True
    )
    endpoint="orders"
    logger.info(f"Getting orders for {store_name}, woocommerce")
    for e in tqdm(range(100)):
        params = {
                'per_page': 50,
                'page': e+1,
                'status':['completed'],#, 'pending payment', 'processing'],
                #'exclude':,
                'orderby':'date',
                'order':'asc',
            }
        resp = wcapi.get(endpoint, params=params).json()
        if resp == []:
            break
        else:
            for item in resp:
                customer_id = Customers.objects.get(customers_code=item['customer_id'], store=store)
                for prod in item['line_items']:
                    try:
                        product_code = ProductAttributes.objects.get(product_code=prod['product_id'], company=store)
                    except ProductAttributes.DoesNotExist as f:
                        logger.error(f)
                        continue
                    try:
                        OrderAttributes.objects.update_or_create(
                            product=product_code,
                            product_qty=prod['quantity'],
                            bill=item['id'],
                            product_name=prod['name'],
                            company=store,
                            defaults={
                                  'user':customer_id
                            }
                            )
                    except IntegrityError as f:
                        logger.error(f)
                        continue
        time.sleep(2)