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
    fhand = open('api/quema_quema_products.csv')
    product = csv.reader(fhand)
    next(product)  # Advance past the header
    fhand = open('api/quema_quema_cross.csv')
    cross_sell = csv.reader(fhand)
    next(cross_sell)  # Advance past the header
    fhand = open('api/quema_quema_upselling.csv')
    up_sell = csv.reader(fhand)
    next(up_sell)  # Advance past the header
    for row in tqdm(product):
        logger.info(row)
        p, created = ProductAttributes.objects.get_or_create(product_id=row[0], name=row[1], sku=row[2], price=row[3] if row[3]!='' else None, permalink=row[4], stock_quantity=row[5], status=row[6], company=row[7], href=row[8], created_at=row[9], updated_at=row[10])
        for up in up_sell:
            if up[0] == row[0]:
                u = UpSellPredictions(product_code=p, recommended_code=p, distance=up[2], created_at=up[3], updated_at=up[4], company=up[5])
                u.save()
        for cross in cross_sell:
            if cross[0] == row[0]:
                c = CrossSellPredictions(product_code=p, recommended_code=p, distance=cross[2], created_at=cross[3], updated_at=cross[4], company=cross[5])
                c.save()
        
    
    