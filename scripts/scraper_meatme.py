import requests as req
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm
import pandas as pd
import json 
from google.cloud import storage
import os
from tqdm import tqdm
from store.models import Store
from django.db.utils import IntegrityError
from django.utils import timezone
from products.models import ProductAttributes
import pytz

SITE_METADATA = {
        'meatme': {
            'base_url': "https://www.meatme.cl",
            'category': "/catalogo/categoria/carnes/wagyu_5/",
            'product_class': "product-pod",
            'product_tag': 'article',
            'next_page_product': "btn-pagination",
            'menu_class': "dropdown-menu megamenu",
            'html': {
                'name': {"tag": "h3", "class_dict": {"class": 'title'}},
                'href': {"tag": "img", "src": "src"},
                'permalink': {"tag": "a", "src": 'href'},
                'price': {"tag": "p", "class_dict": {"class": 'price'}},
                'sku': None
            }
        },
        'sparta': {
            'base_url': "https://www.sparta.cl/",
            'category': "deportes/zapatillas/zapatillas-running.html",
            'product_class': "item product product-item",
            'product_tag': 'li',
            'next_page_product': "btn-pagination",
            'menu_class': "dropdown-menu megamenu",
            'html': {
                'name': {"tag": "a", "class_dict": {"class": 'product-item-link'}},
                'href': {"tag": "img", "src": "src"},
                'permalink': {"tag": "a", "src": 'href'},
                'price': {"tag": "span", "class_dict": {"class": 'price-per-kilo'}},
                'sku': None
            }
        }
}

def get_categories(client):
    '''
    given a category selection this function downloads the product attributes
    '''
    url = f"{SITE_METADATA[client]['base_url']}{SITE_METADATA[client]['category']}"
    res = req.get(url)
    soup = BeautifulSoup(res.text)
    menu_class = SITE_METADATA[client]['menu_class']
    menus = soup.find_all("div", {"class": menu_class})
    categories = []
    for menu in menus:
        for menu_item in menu.find_all("li"):
            categories.append(menu_item.find("a").get("href"))
    return categories

def get_products_from_category(client, category):
    '''
    Given a category selection this function downloads the product attributes
    '''
    if 'http' in category:
        url = category
    else:
        url = f"{SITE_METADATA[client]['base_url']}{category}"
    company = Store.objects.get(company=client)
    res = req.get(url)
    soup = BeautifulSoup(res.text)
    product_class = SITE_METADATA[client]['product_class']
    product_tag = SITE_METADATA[client]['product_tag']
    product_divs = soup.find_all(product_tag, {"class": product_class})
    product_res = []
    for e, product in enumerate(product_divs):
        prod_attributes = {}
        for key in SITE_METADATA[client]['html']:
            if SITE_METADATA[client]['html'][key] is not None:
                if 'class_dict' in SITE_METADATA[client]['html'][key]:
                    p = product.find(SITE_METADATA[client]['html'][key]['tag'], SITE_METADATA[client]['html'][key]['class_dict'])
                    if p is not None:
                        prod_attributes[key] = p.text.strip()
                    else:
                        prod_attributes['error'] = 'product not found'
                elif 'src' in SITE_METADATA[client]['html'][key]:
                    prod_attributes[key] = product.find(SITE_METADATA[client]['html'][key]['tag']).get(SITE_METADATA[client]['html'][key]['src'])
        try:
            prod_attributes['unit'] = prod_attributes['price'].split('/')[1].strip() if len(prod_attributes['price'].split('/')) > 1 else None
            prod_attributes['price'] = int(prod_attributes['price'].split('/')[0].strip().replace('$', '').replace('.', ''))
        except ValueError as err:
            print(err)
            continue

        try:
            ProductAttributes.objects.update_or_create(
                name=prod_attributes['name'],
                permalink=prod_attributes['permalink'],
                company=company,
                defaults={
                    'product_code': 100,
                    'sku': f"{category}{e}",
                    'img_url': prod_attributes['href'],
                    'stock_quantity': True,
                    'status': 'Published',
                    'price': prod_attributes['price'],
                    'product_created_at': timezone.now()
                }
            )
        except IntegrityError as f:
            print(f)
            continue

    return product_res

def get_product_catalog(client, categories=None):
    if categories is None:
        categories = get_categories(client)
    products = []
    for category in tqdm(categories):
        product = get_products_from_category(client, category)
        
        products += product.copy()
    return products


def run(*args):
    client = 'meatme'
    res = get_product_catalog(client)
        
