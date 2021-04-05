import json
from zeep import Client
from zeep.exceptions import Fault
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from tqdm import tqdm
import pandas as pd
from django.db.utils import IntegrityError
from store.models import Store
from products.models import ProductAttributes

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
prat_product_gs = "scripts/productos_prat.csv"

def run(*args):
    company_name = args[0]
    company = Store.objects.get(company=company_name)
    consumer_key = company.consumer_key
    consumer_secret = company.consumer_secret
    logger.info("Getting products")
    wsdl_url = company.api_url
    soap_client = Client(wsdl=wsdl_url) 
    session = soap_client.service.login(consumer_key, consumer_secret)
    logger.info("Downloading all products")
    lista_productos = pd.read_csv(prat_product_gs, names = ["skus"], header=None)["skus"].to_list()
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
                    stock = 1
                else:
                    stock = 0
            try:
                ProductAttributes.objects.update_or_create(
                    product_code=result["product_id"],
                    sku=result["sku"],
                    company=company,
                    defaults={
                        'name':result["name"],
                        'permalink': f"https://www.ferreteriaprat.cl/{result['url_path']}",
                        'img_url': image_url,
                        'stock_quantity': stock,
                        'status': result["status"],
                        'price': int(result["price"].split(".")[0]),
                        'product_created_at': result['created_at']
                    }
                )
            except IntegrityError as f:
                logger.error(f)
                continue
        