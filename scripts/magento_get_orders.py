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

df = pd.read_csv("scripts/prat_orders.csv")
df = pd.read_csv("scripts/orders_construplaza.csv")

def run():
    company_name = 'construplaza'
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