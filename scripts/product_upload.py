import csv  # https://docs.python.org/3/library/csv.html
# https://django-extensions.readthedocs.io/en/latest/runscript.html
# python3 manage.py runscript cats_load
import logging
from datetime import datetime
from tqdm import tqdm
from google.cloud import storage
from google.oauth2 import service_account
from api.models import CrossSellPredictions, UpSellPredictions, ProductAttributes

DATE = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f'./scripts/logs/test_{DATE}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

KEY_PATH = "cactusco/service_account_key.json"
BUCKET_NAME = "cactus_recommender"

credentials = service_account.Credentials.from_service_account_file(
    KEY_PATH, scopes=["https://www.googleapis.com/auth/cloud-platform"],
)


def run(*args):
    client_name = args[0]
    client = storage.Client(credentials=credentials, project=credentials.project_id)
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(f"{client_name}/{client_name}_products.csv")
    blob.download_to_filename(f'./scripts/data/{client_name}_products.csv')
    blob = bucket.blob(f"{client_name}/{client_name}_cross.csv")
    blob.download_to_filename(f'./scripts/data/{client_name}_cross.csv')
    blob = bucket.blob(f"{client_name}/{client_name}_up.csv")
    blob.download_to_filename(f'./scripts/data/{client_name}_up.csv')
    logger.info(f"Process {client_name}")
    fhand = open(f'./scripts/data/{client_name}_products.csv')
    product = csv.reader(fhand)
    fhand = open(f'./scripts/data/{client_name}_cross.csv')
    cross_sell = csv.reader(fhand)
    fhand = open(f'./scripts/data/{client_name}_up.csv')
    up_sell = csv.reader(fhand)
    # Subir todos los productos a ProductAttributes
    for e, row in tqdm(enumerate(product)):
        if e == 0:
            logger.info("Reading products. Fields:")
            logger.info(", ".join(row))
        else:
            sku = row[2]
            if row[2] == '':
                sku = row[0]
            p, _ = ProductAttributes.objects.update_or_create(
                product_code=row[0],
                name=row[1],
                sku=sku,
                permalink=row[4],
                company=row[7],
                href=row[8],
                defaults={
                    'stock_quantity': row[5],
                    'status': row[6],
                    'price': row[3] if row[3] else None
                }
            )

    # Iterar sobre los UpSells y subirlos, relacionando el product_code con el ID
    in_upsell = []
    for e, up in tqdm(enumerate(up_sell)):
        if e == 0:
            logger.info("Reading Up Sells. Fields:")
            logger.info(", ".join(up))
        else:
            if up[0] not in in_upsell:
                in_upsell.append(up[0])
                original_product = ProductAttributes.objects.get(
                    product_code=up[0], 
                    company=client_name
                    )
                UpSellPredictions.objects.filter(
                    product_code=original_product, 
                    company=client_name
                    ).delete()
            original_product = ProductAttributes.objects.get(
                product_code=up[0], 
                company=client_name
                )
            related_product = ProductAttributes.objects.get(
                product_code=up[1],
                company=client_name
                )
            us = UpSellPredictions.objects.update_or_create(
                product_code=original_product, 
                recommended_code=related_product,                 
                company=up[5],
                defaults={
                    'distance': up[2],
                }
                )
    in_cross = []
    for e, cross in tqdm(enumerate(cross_sell)):
        if e == 0:
            logger.info("Reading Cross. Fields:")
            logger.info(", ".join(cross))
        else:
            if cross[0] not in in_cross:
                in_cross.append(cross[0])
                original_product = ProductAttributes.objects.get(
                    product_code=cross[0], 
                    company=client_name
                    )
                CrossSellPredictions.objects.filter(
                    product_code=original_product, 
                    company=client_name
                    ).delete()
            original_product = ProductAttributes.objects.get(
                product_code=cross[0], 
                company=client_name
                )
            related_product = ProductAttributes.objects.get(
                product_code=cross[1], 
                company=client_name
                )
            
            cs = CrossSellPredictions.objects.update_or_create(
                product_code=original_product, 
                recommended_code=related_product,  
                company=cross[5],
                defaults={
                    'distance': cross[2],
                }
            )   
    
    