import json
import timeit
import datetime
import os
import oauth2 as oauth
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / 'integrations' / 'magento' / '.magento-env'
load_dotenv(dotenv_path=env_path)

CONSUMER_KEY = os.getenv('MAGENTO_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('MAGENTO_CONSUMER_SECRET')
TOKEN = os.getenv('MAGENTO_TOKEN')
SECRET = os.getenv('MAGENTO_SECRET')
# your domain here
API_URL = 'https://magento23.reversso.dev/index.php/rest/V1/'


client = None

sku1 = "MS09"
sku2 = "MS09-XS-Black"

productdata = {
  "items": [
    {
      "sku": sku1,
      "link_type": "upsell",
      "linked_product_sku": sku2,
      "linked_product_type": "simple",
      "position": 0,
      "extension_attributes": {
        "qty": 2
      }
    }
  ]
}

delete_related_prods = {  
   "product":{  
      "product_links": [
       
    ]
   }
}

#types of links
#$linkTypes = ['related' => 1, 'upsell' => 4, 'crosssell' => 5, 'associated' => 3];

def setup():
    global client
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=TOKEN, secret=SECRET)

    client = oauth.Client(consumer, token)
    pass


def post_related_product():
    global client
    headers = {'Authorization':f'Bearer {TOKEN}','Accept': 'application/json', 'Content-Type': 'application/json'}
    resp, content = client.request(
        API_URL + f'products/{sku1}/links',
        method='POST', headers=headers, body=json.dumps(productdata).encode("utf-8"))
    print(resp)
    print(content)

def delete_related_product():
    global client

    headers = {'Authorization':f'Bearer {TOKEN}','Accept': 'application/json', 'Content-Type': 'application/json'}
    resp, content = client.request(
        API_URL + f'products/{sku1}/',
        method='PUT', headers=headers, body=json.loads(delete_related_prods))

if __name__ == '__main__':
    print('Session Setup:')
    print(timeit.timeit('setup()',
                        setup='from __main__ import setup',
                        number=1))
    print('Posting related product')
    print(timeit.timeit('post_related_product()',
                        setup='from __main__ import post_related_product',
                        number=1))