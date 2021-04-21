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

base_urls = {
    "protteina": "https://protteina.com/products/",
    "amantani": "https://amantanitienda.cl/products/",
    "pippa": "https://pippa.cl/products/",
}

def get_next_url(headers):
    if 'Link' not in headers:
        return None

    next_section = headers['Link'].split(',')[-1]
    next_section_url = next_section.split(';')[0]
    next_section_type = next_section.split(';')[1]
    new_api_url_clean = next_section_url.replace("<https://", "").replace(">", "").strip()
    rel = next_section_type.split('=')[1].strip('"')
    if rel == 'next':
        return new_api_url_clean
    return None

def get_products(store_name, url=None):
    store = Store.objects.get(company=store_name)
    api_client = store.consumer_key
    api_secret = store.consumer_secret
    api_url = store.api_url
    if url is None:
        logger.info(f"getting products for {store_name}, shopify")
        resource = 'products'
        base_url = f"https://{api_client}:{api_secret}@{api_url}/"
        url =  f"{base_url}/{resource}.json"
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    products = data['products']
    for product in tqdm(products):
        status = status2bool[product['status']] if 'status' in product else False
        status = status if product['published_at'] is not None else False
        try:
            ProductAttributes.objects.update_or_create(
                name=product['title'],
                company=store,
                permalink= base_urls[store.company] + product['handle'],
                defaults={
                    'product_code': product['id'],
                    'sku': product['variants'][0]['sku'],
                    'img_url': product['image']['src'] if 'image' in product else None,
                    'stock_quantity': True if product['variants'][0]['inventory_quantity'] > 0 else False,
                    'status': status,
                    'price': product['variants'][0]['price'],
                    'compare_at_price': product['variants'][0]['compare_at_price'],
                    'product_created_at': product['created_at']
                }
            )
        except TypeError as e:
            print(e)
            print(product)
        except ProductAttributes.MultipleObjectsReturned as f:
            print(f)
            print(product['title'])

    new_api_url_clean = get_next_url(r.headers)
    next_url = f"https://{api_client}:{api_secret}@{new_api_url_clean}" 
    if new_api_url_clean:
        logger.info('new page found, getting products')
        get_products(store_name, next_url)
        
    return None

def get_orders(store_name, url=None):
    store = Store.objects.get(company=store_name)
    api_client = store.consumer_key
    api_secret = store.consumer_secret
    api_url = store.api_url
    if url is None:
        logger.info(f"getting orders for {store_name}, shopify")
        resource = 'orders'
        base_url = f"https://{api_client}:{api_secret}@{api_url}/"
        url =  f"{base_url}/{resource}.json"
    r = requests.get(url)
    data = json.loads(r.text)
    orders = data['orders']
    for order in tqdm(orders):
        for product in order['line_items']:
            try:
                product_code = ProductAttributes.objects.get(product_code=product['product_id'], company=store)
            except ProductAttributes.DoesNotExist as f:
                print(f)
                print(product)
                continue

            OrderAttributes.objects.update_or_create(
                    user=order['email'],
                    product=product_code,
                    product_qty=product['quantity'],
                    bill=order['order_number'],
                    product_name=product['title'],
                    company=store
                )
    
    new_api_url_clean = get_next_url(r.headers)
    next_url = f"https://{api_client}:{api_secret}@{new_api_url_clean}" 
    if new_api_url_clean:
        get_orders(store_name, next_url)
    
    return None
