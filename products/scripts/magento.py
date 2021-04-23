import json
from datetime import datetime
import pandas as pd
import os
import logging
import time
from tqdm import tqdm
from zeep import Client
from zeep.exceptions import Fault
import requests
from bs4 import BeautifulSoup
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from products.models import OrderAttributes, ProductAttributes
from store.models import Store, Customers, Integration


date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


base_urls = {
    'prat':"https://www.ferreteriaprat.cl/",
    'construplaza':"https://www.construplaza.cl/"
}


def get_products(store_name):
    products = f"products/scripts/magento/products_{store_name}.csv"
    store = Store.objects.get(company=store_name)
    store_credentials = Integration.objects.get(store=store)
    consumer_key = store_credentials.consumer_key
    consumer_secret = store_credentials.consumer_secret
    wsdl_url = store_credentials.api_url
    soap_client = Client(wsdl=wsdl_url) 
    session = soap_client.service.login(consumer_key, consumer_secret)
    logger.info(f"Gettting all products for {store_name}")
    lista_productos = pd.read_csv(products, names = ["skus"], header=None)["skus"].to_list()
    for prod in tqdm(lista_productos):
        try:
            result = soap_client.service.catalogProductInfo(session, prod)
        except Fault as f:
            logger.error(f)
            continue
        url = base_urls[store_name] + result['url_path']
        print(url)
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        non_existing = soup.find(text="esta página no está disponible o no existe.")
        logger.info(f"{non_existing}, {url}")
        if non_existing is None:
            image_url = soup.find("a", {"class":"cloud-zoom"})
            if image_url is not None:
                image_url = image_url.get('href')
            stock = soup.find("p", {"class":"availability in-stock"})
            if stock is not None:
                stock = stock.text
                if stock == "Producto Disponible":
                    stock = True
                else:
                    stock = False
            discounted_price =  soup.find("p", {"class":"special-price"})
            if discounted_price is not None:
                discounted_price = discounted_price.find("span", {"class":"price"})
                discounted_price = discounted_price.text.strip().split(" ")[0].replace('$','').replace('.','')
            else:
                discounted_price = None
            try:
                ProductAttributes.objects.update_or_create(
                    company=store,
                    name=result["name"],
                    defaults={
                        'product_code':result["product_id"],
                        'sku':result["sku"],
                        'permalink': url,
                        'img_url': image_url,
                        'stock_quantity': stock,
                        'status': result["status"],
                        'price': discounted_price if discounted_price else int(result["price"][0]),
                        'compare_at_price': int(result["price"].split(".")[0]) if discounted_price else None,
                        'product_created_at': result['created_at']
                    }
                )
            except IntegrityError as f:
                logger.error(f)
                continue


def get_customers(store_name):
    df = pd.read_csv(f"scripts/magento/orders_{store_name}.csv")
    store = Store.objects.get(company=store_name)
    logger.info(f"Getting orders for {store_name}")
    for e, row in tqdm(df.iterrows()):
        if row['Estado'] in ['Pagado', 'Preparación', 'Recibido', 'Retiro', 'Despachado']:
            nombre = row['Nombre del cliente'].split(' ')[0] if row['Nombre del cliente'].split(' ')[0] else None
            apellido = row['Nombre del cliente'].split(' ')[1] if row['Nombre del cliente'].split(' ')[1] else None
            try:
                Customers.objects.update_or_create(
                    customer_code = row['Rut'].replace('.','').replace('-','').replace('k','0').replace('K','0'),
                    store = store,
                    name =  nombre,
                    last_name = apellido,                                
                    defaults={
                        'accepts_marketing': True,
                        'email': None, 
                    }
                    )
            except IntegrityError as f:
                logger.error(f)
                continue
    


def get_orders(store_name):
    df = pd.read_csv(f"scripts/magento/orders_{store_name}.csv")
    store = Store.objects.get(company=store_name)
    logger.info(f"Getting orders for {store_name}")
    for e, row in tqdm(df.iterrows()):
        if row['Estado'] in ['Pagado', 'Preparación', 'Recibido', 'Retiro', 'Despachado']:
            rut = row['Rut'].replace('.','').replace('-','').replace('k','0').replace('K','0')
            customer_id = Customers.objects.get(customers_code=rut, store=store)
            try:
                product_code = ProductAttributes.objects.get(sku=row['SKU'], company=store)
            except ProductAttributes.DoesNotExist as f:
                logger.error(f)
                continue
            try:
                OrderAttributes.objects.update_or_create(
                    customer=customer_id,
                    product=product_code,
                    product_qty=row['Cantidad'],
                    bill=row['ID Pedido'],
                    product_name=row['Producto'],
                    company=store
                    )
            except IntegrityError as f:
                logger.error(f)
                continue

