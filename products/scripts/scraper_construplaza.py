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

def get_product(sku):
    search_url = f"https://www.construplaza.cl/catalogsearch/result/?q={sku}"
    href = "body > div.wrapper > div.page.backgroundMTS > div > div:nth-child(3) > div.col-main > div > div.category-products > ul > li > div > div.product-info > div.containerNombreYMarca > h2 > a"
    response = req.get(search_url)
    html = BeautifulSoup(response.text)
    if html.find('p', {'class':'note-msg sinResultados'}):
        url = None
    else:
        url = html.select(href)[0].get('href')
    return url

def get_name(product_html):
    name = product_html.find('div', {'class':'product-name'}).text.strip()
    return name

def get_sku(product_html):
    sku = product_html.find('div', {'class':'productSKU'}).text.split(":")[1].strip()
    return sku

def get_img(product_html):
    img_url = product_html.find('p', {'class':'product-image'}).find('a')
    if img_url is not None:
        img_url = img_url.get('href')
    return img_url

def get_stock(product_html):
    stock = product_html.find('div', {'class':'extrahints'}).find('p').text
    if stock == "Producto No Disponible":
        stock = False
    elif stock == "Producto Disponible":
        stock = True
    return stock

def get_price(product_html):
    original_price = product_html.find('p', {'class':'old-price'})
    if original_price is not None:
        original_price = original_price.find('span', {'class':'price'}).text.strip().replace("$", "").replace(".","")
        discounted_price = product_html.find('p', {'class':'special-price'}).find('span', {'class':'price'}).text.strip().replace("$", "").replace(".","")
    original_price = product_html.find("span", {'class':'price'}).text.strip().replace("$", "").replace(".","")
    discounted_price = None
    return [original_price, discounted_price]

def constru_get_products():
    df = pd.read_csv("scripts/products_construplaza.csv", sep=";")
    store_name = "construplaza"
    company = Store.objects.get(company=store_name)
    for e, row in df.iterrows():
        product_url = get_product(row['SKU'])
        if product_url is not None:
            product_res = req.get(product_url)
            product_html = BeautifulSoup(product_res.text, 'html.parser')
            if get_sku(product_html) == row['SKU']:
                try:
                    print(ProductAttributes.objects.update_or_create(
                        name=get_name(product_html),
                        company=company,
                        permalink= product_url,
                        defaults={    
                            'product_code': 100,
                            'sku': get_sku(product_html),
                            'img_url': get_img(product_html),
                            'stock_quantity': get_stock(product_html),
                            'status': True,
                            'discounted_price': get_price(product_html)[1],
                            'price': get_price(product_html)[0],
                            'product_created_at': timezone.now()
                        }
                    ))
                except IntegrityError as f:
                    print(f)
                    #continue