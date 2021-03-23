import csv  # https://docs.python.org/3/library/csv.html
# https://django-extensions.readthedocs.io/en/latest/runscript.html
# python3 manage.py runscript cats_load
import logging
from api.models import CrossSellPredictions, UpSellPredictions, ProductAttributes
from api.serializers import CrossSellPredictionsSerializer, UpSellPredictionsSerializer, ProductAttributesSerializer
from datetime import datetime
from tqdm import tqdm
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

def run():
    client = 'makerschile'
    fhand = open(f'./api/{client}_products.csv')
    product = csv.reader(fhand)

    fhand = open(f'api/{client}_cross.csv')
    cross_sell = csv.reader(fhand)
    fhand = open(f'api/{client}_up.csv')
    up_sell = csv.reader(fhand)

    # Subir todos los productos a ProductAttributes
    for e, row in tqdm(enumerate(product)):
        if e == 0:
            logger.info("Reading products. Fields:")
            logger.info(", ".join(row))
        else:
            p, created = ProductAttributes.objects.get_or_create(product_code=row[0], name=row[1], sku=row[0], price=row[3] if row[3]!='' else None, permalink=row[4], stock_quantity=row[5], status=row[6], company=row[7], href=row[8], created_at=row[9], updated_at=row[10])

    # Iterar sobre los UpSells y subirlos, relacionando el product_code con el ID
    for e, up in tqdm(enumerate(up_sell)):
        if e == 0:
            logger.info("Reading Up Sells. Fields:")
            logger.info(", ".join(up))
        else:
            original_product = ProductAttributes.objects.get(product_code=up[0], company=client)
            related_product = ProductAttributes.objects.get(product_code=up[1], company=client)
            us = UpSellPredictions(product_code=original_product, recommended_code=related_product, distance=up[2], created_at=up[3], updated_at=up[4], company=up[5])
            us.save()

    for e, cross in tqdm(enumerate(cross_sell)):
        if e == 0:
            logger.info("Reading Cross. Fields:")
            logger.info(", ".join(cross))
        else:
            original_product = ProductAttributes.objects.get(product_code=cross[0], company=client)
            related_product = ProductAttributes.objects.get(product_code=cross[1], company=client)
            
            cs = CrossSellPredictions(product_code=original_product, recommended_code=related_product, distance=cross[0], created_at=cross[3], updated_at=cross[4], company=cross[5])
            cs.save()
            
    
    