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
from store.models import Store


date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f'./scripts/magento/logs/log_{date}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def get_products(company_name):
    products = f"products/scripts/magento/products_{company_name}.csv"
    company = Store.objects.get(company=company_name)
    consumer_key = company.consumer_key
    consumer_secret = company.consumer_secret
    logger.info("Getting products")
    wsdl_url = company.api_url
    soap_client = Client(wsdl=wsdl_url) 
    session = soap_client.service.login(consumer_key, consumer_secret)
    logger.info("Downloading all products")
    lista_productos = pd.read_csv(products, names = ["skus"], header=None)["skus"].to_list()
    for e, prod in enumerate(tqdm(lista_productos)):
        try:
            result = soap_client.service.catalogProductInfo(session, prod)
        except Fault as f:
            logger.error(f)
            continue
        url = result['url_path']
        req = requests.get(f"https://www.ferreteriaprat.cl/{url}")
        soup = BeautifulSoup(req.text, 'html.parser')
        non_existing = soup.find(text="esta página no está disponible o no existe.")
        logger.info(f"{non_existing}, https://www.ferreteriaprat.cl/{result['url_path']}")
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
                    company=company,
                    name=result["name"],
                    defaults={
                        'product_code':result["product_id"],
                        'sku':result["sku"],
                        'permalink': f"https://www.ferreteriaprat.cl/{result['url_path']}",
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


def get_orders(company_name):
    df = pd.read_csv(f"scripts/magento/orders_{company_name}.csv")
    company = Store.objects.get(company=company_name)
    logger.info("Getting orders")
    for e, row in tqdm(df.iterrows()):
        if row['Estado'] in ['Pagado', 'Preparación', 'Recibido', 'Retiro', 'Despachado']:
            try:
                product_code = ProductAttributes.objects.get(sku=row['SKU'], company=company)
            except ProductAttributes.DoesNotExist as f:
                logger.error(f)
                continue
            try:
                OrderAttributes.objects.update_or_create(
                    user=row['Rut'].replace('.','').replace('-',''),
                    product=product_code,
                    product_qty=row['Cantidad'],
                    bill=row['ID Pedido'],
                    product_name=row['Producto'],
                    company=company
                    )
            except IntegrityError as f:
                logger.error(f)
                continue