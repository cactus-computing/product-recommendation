import requests as req
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm
import pandas as pd
import json 
import os
from tqdm import tqdm
from store.models import Store
from django.db.utils import IntegrityError
from django.utils import timezone
from products.models import ProductAttributes
import pytz

category_url = "https://www.konstruyendo.com/categorias/cat51000000/materiales-de-construccion"
base_url = "https://www.konstruyendo.com/"
res = req.get(category_url)
category_html = BeautifulSoup(res.text)

def get_categories():
    category_elements = category_html.find_all('li', {'class': 'cat-item'})
    category_links = []
    for cat_element in category_elements:
        category_links += [ base_url +  cat_element.find('a').get('href')]
    return category_links

def get_products(store_name):
    categories = get_categories()
    for category in tqdm(categories):
        category_res = req.get(category)
        catalog_html = BeautifulSoup(category_res.text, 'html.parser')
        products = catalog_html.find_all('li', {'class': 'product'})
        product_links = []
        company = Store.objects.get(company=store_name)
        for product in products:
            product_url = base_url[:-1] + product.find('a').get('href')
            print(product_url)
            product_res = req.get(product_url)
            product_html = BeautifulSoup(product_res.text, 'html.parser')
            price =  get_price(product_html)
            discounted_price = get_discounted_price(product_html)
            try:
                ProductAttributes.objects.update_or_create(
                    name=get_title(product_html),
                    company=company,
                    permalink=product_url,
                    defaults={
                        'product_code': 100,
                        'sku': get_sku(product_html),
                        'img_url': get_img(product_html),
                        'stock_quantity': get_stock(product_html),
                        'status': True,
                        'compare_at_price': price if discounted_price else None,
                        'price': discounted_price if discounted_price else price,
                        'product_created_at': timezone.now()
                    }
                )
            except IntegrityError as f:
                print(f)
                continue
            except IndexError as ie:
                print(product_url)
                print(ie)
                continue
    
def get_sku(product_html):
    selector = "#main > div > div.single-product-wrapper > div.summary.entry-summary.hidden-xs > div > p"
    element = product_html.select(selector)[0]
    clean_str = element.text.split(':')[1].strip()
    return clean_str
    
def get_price(product_html):
    selector = "#main > div > div.single-product-wrapper > div.product-actions-wrapper > div.product-actions > div > p > span > del > span"
    element = product_html.select(selector)
    if element == []:
        selector = "#main > div > div.single-product-wrapper > div.product-actions-wrapper > div.product-actions > div > p > span > ins > span"
        element = product_html.select(selector)
    element = element[0]
    clean_str = element.text.replace('$', '').replace('.', '')
    return clean_str

def get_discounted_price(product_html):
    selector = "#main > div > div.single-product-wrapper > div.product-actions-wrapper > div.product-actions > div > p > span > ins > span"
    element = product_html.select(selector)
    if element == []:
        return None
    element = element[0]
    clean_str = element.text.replace('$', '').replace('.', '')
    return clean_str


def get_stock(product_html):
    selector = "#main > div > div.single-product-wrapper > div.product-actions-wrapper > div.product-actions > form > div > div.woocommerce-variation-add-to-cart.variations_button > a"
    element = product_html.select(selector)[0]
    clean_str = element.text
    if clean_str == 'Agregar al Carro':
        stock = True
    else:
        stock = False
    return stock

def get_title(product_html):
    selector = "#main > div > div.single-product-wrapper > div.summary.entry-summary.hidden-xs > h1"
    element = product_html.select(selector)[0]
    clean_str = element.text
    return clean_str

def get_img(product_html):
    img_class_name = "wp-post-image"
    element = product_html.find("img", img_class_name)
    clean_str = element.get('src')
    return clean_str
