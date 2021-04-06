import tensorflow_hub as hub
import pandas as pd
import time
from .model_common import get_top_k_for_each, send_to_db, get_products_df
import logging

from products.models import UpSellPredictions

ITEM = 'id'
NAME = 'name'

K = 30

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

logger = logging.getLogger(__name__)

def upselling_pipeline(products_df, item_encoded2item, k):
    
    logger.info("Retrieving the Universal Sentence Encoder model from tf hub")
    sentence_encoder_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    embed = hub.load(sentence_encoder_url)

    logger.info("Generate Embeddings")
    embeddings = embed(products_df[[ITEM, NAME]].drop_duplicates(subset=[ITEM])[NAME].tolist()).numpy()

    up_selling = get_top_k_for_each(embeddings, item_encoded2item.keys(), k=k, method='dot')

    run_id = time.strftime("run_%Y%m%d")
    
    return up_selling, run_id


def run(*arg):

    if arg[0] == 'all':
        companies = ['quema', 'makers', 'pippa', 'prat']
    else:
        companies = [ arg[0] ]
        
    for company in companies:
        logger.info(f"Running model for {company}")
        products_df = get_products_df(company)

        items = products_df[ITEM].unique().tolist()
        item2item_encoded = {k: e for e, k in enumerate(items)}
        item_encoded2item =  {item2item_encoded[k]: k for k in item2item_encoded}
        item2item_name = products_df[[ITEM, NAME]].drop_duplicates(subset=[ITEM]).set_index(ITEM).to_dict()[NAME]

        us, _ = upselling_pipeline(products_df, item_encoded2item, k=K)

        us["product_id"] = us.product_id.map(item_encoded2item)
        us["recommended_id"] = us.recommended_id.map(item_encoded2item)

        us["product_name"] = us.product_id.map(item2item_name)
        us["recommended_name"] = us.recommended_id.map(item2item_name)

        send_to_db(us, company_name=company, django_model=UpSellPredictions)