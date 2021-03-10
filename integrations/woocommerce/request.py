import json
import os
import oauth2 as oauth
from pathlib import Path
from dotenv import load_dotenv
from woocommerce import API

env_path = Path('.') / 'integrations' / 'woocommerce' / '.woocommerce-env'
load_dotenv(dotenv_path=env_path)

# oauth constants - enter yours here
CONSUMER_KEY = os.getenv('WOOCOMMERCE_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('WOOCOMMERCE_CONSUMER_SECRET')
# your domain here
API_URL = 'https://ecommerce.cactusco.cl/'

wcapi = API(
    url=API_URL,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    version="wc/v3"
)
endpoint = "orders"
resp = wcapi.get(endpoint).json()
with open('./integrations/woocommerce/orders.json', 'w+') as f:
    f.write(json.dumps(resp))

endpoint = "products"
resp = wcapi.get(endpoint).json()
with open('./integrations/woocommerce/products.json', 'w+') as f:
    f.write(json.dumps(resp))


data = {
    "upsell_ids": ["18"],
    "cross_sell_ids": ["12"]
}

id_producto = "14"
print(wcapi.put(f"products/{id_producto}", data).json())
