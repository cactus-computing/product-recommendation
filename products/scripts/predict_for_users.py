import tensorflow_hub as hub
import pandas as pd
from .model_common import get_top_k_for_each, send_to_db, send_personalization_to_db, get_orders, train_collaborative_filters
import logging
import time
from products.models import CrossSellPredictions, ProductAttributes, CustomerPredictions
from store.models import Store, Customers

BUCKET = 'cactus_recommender'

ITEM = 'product_id'
NAME = 'product_name'
BILL = 'bill'
USER = 'customer'
QTY = 'product_qty'

K = 30


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

def train_cross_sell(ratings, n, m, client):
    '''
    Gets the predictions for each product of the store. 
    Uploads results to google cloud storage
    '''
    logger.info('initializing cross selling script')
    model, _ = train_collaborative_filters(ratings, n, m, client, build=True)

    run_id = time.strftime("run_%Y%m%d")
            
    return model, run_id


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
        user_encoded2user =  {user2user_encoded[k]: k for k in user2user_encoded}


        logger.info("Creating item mapping dictionaries")
        items = df[ITEM].unique().tolist()
        logger.info(f"{items[0]}")
        item2item_encoded = {k: e for e, k in enumerate(items)}
        item_encoded2item =  {item2item_encoded[k]: k for k in item2item_encoded}
        item2item_name = df[[ITEM, NAME]].drop_duplicates(subset=[ITEM]).set_index(ITEM).to_dict()[NAME]
        logger.info("Mapping users and items to new id's")
        df[USER] = df[USER].map(user2user_encoded)
        df[ITEM] = df[ITEM].map(item2item_encoded)
        
        
        ratings = df[[USER, ITEM, QTY]]
        ratings = ratings.groupby([USER, ITEM], as_index=False).agg({QTY: 'sum'})

        logger.info(f"Users: {len(users)}, Items: {len(items)} Entries: {ratings.shape[0]}")

        ratings = standarize_ratings(ratings)

        model, _ = train_cross_sell(
            ratings=ratings, 
            n=len(users), 
            m=len(items), 
            client=company
        )
        
        records = []
        logger.info(f"Users: {len(users)}, Items: {len(items)} Entries: {ratings.shape[0]}")
        for user in df[USER].values:
            for item in df[ITEM].values:
                records.append({
                    USER: int(user),
                    ITEM: int(item)
                })

        unrated = pd.DataFrame.from_records(records)
        logger.info(f"Unrated predictions {len(unrated):,}")
        predictions = model.predict(unrated.values)
        unrated['rates'] = predictions[:,0]
        k=20
        unrated_join = unrated.set_index([USER, ITEM]).join(ratings.set_index([USER, ITEM]))
        unrated_join = unrated_join[pd.notna(unrated_join['product_qty'])]
        
        # final output processing
        rated_top_k = unrated.groupby(USER).head(k).sort_values([USER, ITEM], ascending=[True, False])
        rated_top_k[USER] = rated_top_k[USER].map(user_encoded2user)
        rated_top_k[ITEM] = rated_top_k[ITEM].map(item_encoded2item)
        rated_top_k[NAME] = rated_top_k[ITEM].map(item2item_name)
        
        logger.info(f"Top predictions for each user {len(rated_top_k):,}")
        
        send_personalization_to_db(rated_top_k, store_name=company)