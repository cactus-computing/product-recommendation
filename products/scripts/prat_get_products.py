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
        logging.FileHandler('./products/scripts/magento/logs/log_.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
prat_product_gs = "scripts/productos_prat.csv"

def run():
    company_name = 'prat'
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
                    permalink=f"https://www.ferreteriaprat.cl/{result['url_path']}",
                    defaults={
                        'product_code':result["product_id"],
                        'sku':result["sku"],
                        'img_url': image_url,
                        'stock_quantity': stock,
                        'status': result["status"],
                        'price': int(result["price"].split(".")[0]),
                        'discounted_price':discounted_price,
                        'product_created_at': result['created_at']
                    }
                )
            except IntegrityError as f:
                logger.error(f)
                continue
        