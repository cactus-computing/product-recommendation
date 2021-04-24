import tensorflow_hub as hub
import pandas as pd
from .model_common import get_top_k_for_each, send_to_db, get_orders, train_collaborative_filters
import logging
import time
from products.models import CrossSellPredictions, ProductAttributes
from store.models import Store

BUCKET = 'cactus_recommender'

ITEM = 'product_id'
BILL = 'bill'
USER = 'customer'
QTY = 'product_qty'

K = 50
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

logger = logging.getLogger(__name__)


def standarize_ratings(ratings):
    '''
    Treatment for target rating, Currently, it sets the to 1
    '''
    ratings[QTY] = 1
    return ratings

def cross_selling_pipeline(ratings, n, m, client, item_encoded2item, k):
    '''
    Gets the predictions for each product of the store. 
    Uploads results to google cloud storage
    '''
    logger.info('initializing cross selling script')
    model, _ = train_collaborative_filters(ratings, n, m, client, build=True)
    embeddings = model.item_embedding.get_weights()[0]

    cross_selling = get_top_k_for_each(
        embeddings=embeddings,
        ids=list(item_encoded2item.keys()), 
        k=k, 
        method='dot'
    )

    run_id = time.strftime("run_%Y%m%d")
            
    return cross_selling, run_id


def run(*arg):
    logger.info(f"selection: {arg[0]}")
    if arg[0] == 'all':
        companies = ['quema', 'makers', 'pippa', 'prat']
    else:
        companies = [ arg[0] ]

    for company in companies:
        logger.info(f"Running model for {company}")
        logger.info("Downloading orders")
        df = get_orders(company)
        logger.info("OK")
        
        if len(df) == 0:
            logger.info('No data to analyse. Quitting this customer')
            continue
        
        logger.info("Creating user mapping dictionaries")
        users = df[USER].unique().tolist()
        user2user_encoded = {k: e for e, k in enumerate(users)}

        logger.info("Creating item mapping dictionaries")
        items = df[ITEM].unique().tolist()
        logger.info(f"{items[0]}")
        item2item_encoded = {k: e for e, k in enumerate(items)}
        item_encoded2item =  {item2item_encoded[k]: k for k in item2item_encoded}

        logger.info("Mapping users and items to new id's")
        df[USER] = df[USER].map(user2user_encoded)
        df[ITEM] = df[ITEM].map(item2item_encoded)
        
        ratings = df[[USER, ITEM, QTY]]
        ratings = ratings.groupby([USER, ITEM], as_index=False).agg({QTY: 'sum'})

        logger.info(f"Users: {len(users)}, Items: {len(items)} Entries: {ratings.shape[0]}")

        ratings = standarize_ratings(ratings)

        cs, _ = cross_selling_pipeline(
            ratings=ratings, 
            n=len(users), 
            m=len(items), 
            client=company, 
            item_encoded2item=item_encoded2item,
            k=K
        )

        cs["product_id"] = cs.product_id.map(item_encoded2item)
        cs["recommended_id"] = cs.recommended_id.map(item_encoded2item)
        
        send_to_db(cs, company_name=company, django_model=CrossSellPredictions)