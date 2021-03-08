from pathlib import Path
from dotenv import load_dotenv
import os
import requests
import json

env_path = Path('.') / 'integrations' / 'shopify' / '.shopify-env'
load_dotenv(dotenv_path=env_path)

username = os.getenv('SHOPIFY_USERNAME')
password = os.getenv('SHOPIFY_PASS')
shop = os.getenv('SHOPIFY_SHOP_NAME')
api_version = os.getenv('SHOPIFY_API_VERSION')

resource = "orders"

url =  f"https://{username}:{password}@{shop}.myshopify.com/admin/api/{api_version}/{resource}.json"
r = requests.get(url)

json_res = r.json()

with open('./integrations/shopify/res.json', 'w+') as f:
    f.write(json.dumps(json_res))