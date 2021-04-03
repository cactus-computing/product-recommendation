import tensorflow_hub as hub
import pandas as pd
from .model_common import get_top_k_for_each, send_to_db, get_orders, train_collaborative_filters
import logging
import time
from products.models import CrossSellPredictions, ProductAttributes
from store.models import Store

BUCKET = 'cactus_recommender'

ITEM = 'product_name'
BILL = 'bill'
USER = 'user'
QTY = 'product_qty'

K = 30

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
    
    if arg[0] == 'all':
        companies = ['quema', 'makers', 'pippa', 'prat']
    else:
        companies = [ arg[0] ]

    for company in companies:
        logger.info(f"Running model for {company}")
        logger.info("Creating user mapping dictionaries")
        df = get_orders(company)
        
        if len(df) == 0:
            logger.info('No data to analyse. Quitting this customer')
            continue

        users = df[USER].unique().tolist()
        user2user_encoded = {k: e for e, k in enumerate(users)}

        logger.info("Creating item mapping dictionaries")
        items = df[ITEM].unique().tolist()
        item_name2item_encoded = {k: e for e, k in enumerate(items)}
        item_encoded2item_name =  {item_name2item_encoded[k]: k for k in item_name2item_encoded}

        logger.info("Mapping users and items to new id's")
        df[USER] = df[USER].map(user2user_encoded)
        df[ITEM] = df[ITEM].map(item_name2item_encoded)
        
        ratings = df[[USER, ITEM, QTY]]
        ratings = ratings.groupby([USER, ITEM], as_index=False).agg({QTY: 'sum'})

        logger.info(f"Users: {len(users)}, Items: {len(items)} Entries: {ratings.shape[0]}")

        ratings = standarize_ratings(ratings)

        cs, _ = cross_selling_pipeline(
            ratings=ratings, 
            n=len(users), 
            m=len(items), 
            client=company, 
            item_encoded2item=item_encoded2item_name,
            k=K
        )
        
        cs['recommended_name'] = cs.index.map(item_encoded2item_name)
        cs['product_name'] = cs['product_id'].map(item_encoded2item_name)
        
        send_to_db(cs, company_name=company, django_model=CrossSellPredictions)