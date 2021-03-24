import json
from woocommerce import API
from datetime import datetime
from .wc.storage import  upload_blob_to_default_bucket
import os
import logging
import time
from tqdm import tqdm
import glob

with open('./scripts/wc/wc-keys.json') as f:
  keys = json.load(f) 
def run(*args):
    COMPANY = args[0]
    CONSUMER_KEY = keys[COMPANY]["CONSUMER_KEY"]
    CONSUMER_SECRET = keys[COMPANY]["CONSUMER_SECRET"]
    API_URL = keys[COMPANY]["API_URL"]
    DATE = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    wcapi = API(
        url=API_URL,
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        version="wc/v3",
        query_string_auth=True
    )
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(f'./scripts/wc/logs/{COMPANY}_{DATE}.log'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    endpoint="products"
    logger.info("Getting products")
    json_file = []
    for e in tqdm(range(100)):
        params = {
                'per_page': 50,
                'page': e+1,
                'status':['any'],
                'order':'asc',
            }
        resp = wcapi.get(endpoint, params=params).json()
        if resp == []:
            break
        else:
            for item in resp:
                json_file.append(item)
        time.sleep(1)
    blob_name = f"{COMPANY}/{endpoint}.json"
    upload_blob_to_default_bucket(json_file,blob_name)
    if COMPANY == "cactus":
        with open(f'./scripts/wc/{endpoint}.json', 'w+') as f:
            json.dump(json_file, f)



    