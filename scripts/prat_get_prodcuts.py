import json
from zeep import Client
from zeep import xsd
from datetime import datetime
from .wc.storage import  upload_blob_to_default_bucket
import os
import logging
import time
from tqdm import tqdm
import glob

with open('./scripts/magento/magento-keys.json') as f:
  keys = json.load(f) 

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
    filters = [{
        'complex_filter': {
            'complexObjectArray': [{
                'key': 'type',
                'value':{
                'key': 'in', 
                'value': 'simple,configurable'
                }
            }]
        }
    }]
    logger.info("Downloading all products")
    result = soap_client.service.catalogProductList(session, filters)
    logger.info("Done")
    prods = []
    for prod in tqdm(result):
        prods.append(prod['product_id'])
    productos = []
    print("Done")
    for prod in tqdm(prods):
        result = soap_client.service.catalogProductInfo(session, prod)
        #stock = soap_client.service.catalogInventoryStockItemList(session, prod)
        #image = soap_client.service.catalogProductAttributeMediaList(session, prod)
        #print(image['url'])
        image = f"https://www.ferreteriaprat.cl/media/catalog/product/cache/1/image/1200x1200/9df78eab33525d08d6e5fb8d27136e95/{result['sku'][0]}/{result['sku'][1]}/{result['sku']}.jpg"
        print(image)
        result_ = {
            "product_id": result["product_id"],
            "sku": result["sku"],
            "set": result["set"],
            "type": result["type"],
            "name": result["name"],
            "description": result["description"],
            "short_description": result["short_description"],
            "url": f"https://www.ferreteriaprat.cl/{result['url_path']}",
            "img_url": image,#image['url'],
            "status": result["status"],
            "stock_quantity": 1, #stock["qty"],
            "price": result["price"],
            "special_price": result["special_price"]
        }
        print(result_)
        productos.append(result_)
        break
    print(productos)
    blob_name = f"{COMPANY}/products.json"
    upload_blob_to_default_bucket(productos,blob_name)
    with open(f'./scripts/magento/data/products.json', 'w+') as f:
        json.dump(productos, f)



    