import json
from zeep import Client
from zeep.exceptions import Fault
import requests
from bs4 import BeautifulSoup
from zeep import xsd
from datetime import datetime
from .wc.storage import  upload_blob_to_default_bucket, download_blob
import os
import logging
import time
from tqdm import tqdm
import glob
import pandas as pd

with open('./scripts/magento/magento-keys.json') as f:
  keys = json.load(f) 

prat_product_gs = "gs://cactus_recommender/prat/productos_prat.csv"

def run(*args):
    COMPANY = args[0]
    DATE = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(f'./scripts/magento/logs/products_{COMPANY}_{DATE}.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    CONSUMER_KEY = keys[COMPANY]["CONSUMER_KEY"]
    CONSUMER_SECRET = keys[COMPANY]["CONSUMER_SECRET"]
    logger.info("Getting products")
    wsdl_url = "https://www.ferreteriaprat.cl/api/v2_soap/?wsdl"
    soap_client = Client(wsdl=wsdl_url) 
    session = soap_client.service.login(CONSUMER_KEY, CONSUMER_SECRET)
    logger.info("Downloading all products")
    lista_productos = pd.read_csv(prat_product_gs, names = ["skus"], header=None)["skus"].to_list()
    productos = []
    for e, prod in enumerate(tqdm(lista_productos)):
        try:
            result = soap_client.service.catalogProductInfo(session, prod)
        except Fault as e:
            print(e)
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
            result_ = {
                "product_id": result["product_id"],
                "sku": result["sku"],
                "set": result["set"],
                "type": result["type"],
                "name": result["name"],
                "url": f"https://www.ferreteriaprat.cl/{result['url_path']}",
                "img_url": image_url,
                "status": result["status"],
                "stock_quantity": stock,
                "price": int(result["price"].split(".")[0]),
            }
            productos.append(result_)
            logger.info(result_)
    blob_name = f"{COMPANY}/products.json"
    upload_blob_to_default_bucket(productos,blob_name)
    logger.info(f"{len(productos)} uploaded to GCS")



    