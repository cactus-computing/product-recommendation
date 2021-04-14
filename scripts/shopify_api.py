from pathlib import Path
import os
import requests
import json
from tqdm import tqdm
import logging
from store.models import Store
from products.models import ProductAttributes, OrderAttributes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

store = None
api_client = None
api_secret = None
api_url = None

status2bool = {
    'active': True,
   'draft': False
}

def get_next_url(headers):
    if 'Link' not in headers:
        return None
        
    next_section = headers['Link'].split(',')[-1]
    next_section_url = next_section.split(';')[0]
    next_section_type = next_section.split(';')[1]

    new_api_url_clean = next_section_url.replace("<https://", "").replace(">", "").strip()
    new_url_with_auth = f"https://{api_client}:{api_secret}@{new_api_url_clean}" 
    
    rel = next_section_type.split('=')[1].strip('"')

    if rel == 'next':
        return new_url_with_auth
    return None

def get_products(url):
    r = requests.get(url)
    data = json.loads(r.text)
    products = data['products']
    for product in tqdm(products):
        ProductAttributes.objects.update_or_create(
                name=product['title'],
                company=store,
                permalink="https://protteina.com/products/" + product['handle'],
                defaults={
                    'product_code': product['id'],
                    'sku': product['variants'][0]['sku'],
                    'img_url': product['image']['src'],
                    'stock_quantity': True if product['variants'][0]['inventory_quantity'] > 0 else False,
                    'status': status2bool[product['status']],
                    'price': product['variants'][0]['price'],
                    'discounted_price': product['variants'][0]['compare_at_price'],
                    'product_created_at': product['created_at']
                }
            )

    next_url = get_next_url(r.headers)

    if next_url:
        logger.info('new page found, getting products')
        get_products(next_url)
    
    return None

def get_orders(url):
    r = requests.get(url)
    data = json.loads(r.text)
    orders = data['orders']
    for order in tqdm(orders):
        for product in order['line_items']:
            try:
                product_code = ProductAttributes.objects.get(name=product['title'], company=store)
            except ProductAttributes.DoesNotExist as f:
                print(f)
                continue

            OrderAttributes.objects.update_or_create(
                    user=order['email'],
                    product=product_code,
                    product_qty=product['quantity'],
                    bill=order['order_number'],
                    product_name=product['title'],
                    company=store
                )
    
    next_url = get_next_url(r.headers)

    if next_url:
        get_orders(next_url)
    
    return None

def run(*args):
    global store, api_client, api_secret, api_url

    store_name = args[0]

    store = Store.objects.get(company=store_name)
    api_client = store.consumer_key
    api_secret = store.consumer_secret
    api_url = store.api_url

    logger.info("getting products")
    resource = 'products'
    base_url = f"https://{api_client}:{api_secret}@{api_url}/"
    url =  f"{base_url}/{resource}.json"
    get_products(url)

    logger.info("getting orders")
    resource = "orders"
    url =  f"{base_url}/{resource}.json"
    get_orders(url)
