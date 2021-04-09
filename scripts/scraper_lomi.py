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
    
def get_sku(product_html):
    return None
    
def get_price(product_html):
    selector = "#product-price > span.price.selling"
    element = product_html.select(selector)[0]
    clean_str = element.text.replace('$', '').replace('.', '').strip()
    return clean_str

def get_discounted_price(product_html):
    selector = None
    element = None
    clean_str = None
    return None


def get_stock(product_html):
    selector = "#inside-product-cart-form > div.text-center.text-md-left.add-to-cart-form-general-availability.text-uppercase > span"
    element = product_html.select(selector)[0]
    clean_str = element.text
    if clean_str == 'Con Stock':
        stock = True
    else:
        stock = False
    return stock

def get_title(product_html):
    selector = "#product-description > h1"
    element = product_html.select(selector)[0]
    clean_str = element.text.strip()
    return clean_str

def get_img(product_html):
    selector = "#productCarousel > div > div.carousel-item.product-carousel-item.active > div > img"
    element = product_html.select(selector)[0]
    clean_str = element.get('src')
    return clean_str

def get_product_details(product_soup):
    return json.dumps({ 
        'name': get_title(product_soup),
        #'company': store_name,
        #'permalink': product_url,
        'sku': get_sku(product_soup),
        'img_url': get_img(product_soup),
        'stock_quantity': get_stock(product_soup),
        'status': 'Published',
        'discounted_price': get_discounted_price(product_soup),
        'price': get_price(product_soup),
        #'product_created_at': timezone.now()
    }, indent=2, default=str)
    
def get_categories(base_url):
    category_html = BeautifulSoup(req.get(base_url).text)
    category_elements = category_html.find_all('a', {'class': 'dropdown-item primary-color-text text-bold'})
    category_links = []
    for cat_element in category_elements:
        category_links += [ base_url +  cat_element.get('href')]
    return category_links
    
def get_products_from_category(base_url, store_name, categories):
    global product_count
    for category in tqdm(categories):
        category_res = req.get(category)
        catalog_html = BeautifulSoup(category_res.text, 'html.parser')
        product_selector = "#product_547 > div > a"
        product_links = catalog_html.find_all("a", {"class": "text-body"})
        store_object = Store.objects.get(company=store_name)
        for link in product_links:
            product_url = base_url + link.get('href')
            product_res = req.get(product_url)
            product_html = BeautifulSoup(product_res.text, 'html.parser')
            try:
                ProductAttributes.objects.update_or_create(
                    name=get_title(product_html),
                    company=store_object,
                    defaults={
                        'permalink': product_url,
                        'product_code': product_count,
                        'sku': get_sku(product_html),
                        'img_url': get_img(product_html),
                        'stock_quantity': get_stock(product_html),
                        'status': 'Published',
                        'discounted_price': get_discounted_price(product_html),
                        'price': get_price(product_html),
                        'product_created_at': timezone.now()
                    }
                )
                product_count += 1
            except IntegrityError as f:
                print(f)
                continue
            except IndexError as ie:
                print(product_url)
                print(ie)
                continue


product_count = 0

def run(*args):
    store_name = 'lomi'
    base_url = 'https://lomi.cl'

    product_url = "https://lomi.cl/products/aceite-de-oliva-light-arbequina?taxon_id=155"
    product_html = req.get(product_url, 'html.parser').text
    categories = get_categories(base_url)
    get_products_from_category(base_url, store_name, categories)
    print(f"Total scraped products {product_count}")
        


