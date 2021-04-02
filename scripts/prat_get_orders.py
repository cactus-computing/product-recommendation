import json
from datetime import datetime
import pandas as pd
import os
import logging
import time
from tqdm import tqdm
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from products.models import OrderAttributes, ProductAttributes
from store.models import Store

with open('./scripts/magento/magento-keys.json') as f:
  keys = json.load(f) 

files_1 = "gs://cactus_recommender/prat/orders/Ene-abr-2020.csv"
files_2 = "gs://cactus_recommender/prat/orders/May-Ago-2020.csv"
files_3 = "gs://cactus_recommender/prat/orders/Sep2020-Mar2021.csv"
df = pd.concat([pd.read_csv(files_1),pd.read_csv(files_2),pd.read_csv(files_3)])[['Rut','Estado','Comprado en','Cantidad','ID Pedido','Producto']]
df.dropna(inplace=True)
def run(*args):
    COMPANY_NAME = args[0]
    company = Store.objects.get(company=COMPANY_NAME)
    DATE = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(f'./scripts/wc/logs/{COMPANY_NAME}_{DATE}.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
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
                    company=company,
                    record_created_at=datetime.datetime.strptime(row['Created_at'], '%Y-%m-%d %H:%M:%S.%f')
                    )
            except IntegrityError as f:
                logger.error(f)
                continue