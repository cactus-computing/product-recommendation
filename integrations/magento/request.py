import json
import timeit
import datetime
import os
import oauth2 as oauth
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / 'integrations' / 'magento' / '.magento-env'
load_dotenv(dotenv_path=env_path)

# oauth constants - enter yours here
CONSUMER_KEY = os.getenv('MAGENTO_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('MAGENTO_CONSUMER_SECRET')
#REQUEST_TOKEN = 'nh0bzbc0toxzjyn9d7yo84qchf904uq2'
TOKEN = os.getenv('MAGENTO_TOKEN')
SECRET = os.getenv('MAGENTO_SECRET')
# your domain here
API_URL = 'https://magento23.reversso.dev/index.php/rest'


client = None


def setup():
    global client
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=TOKEN, secret=SECRET)

    client = oauth.Client(consumer, token)
    pass


def get_sales_data():
    global client
    #name = 'Blackberry Playbook 7" WiFi Tablet - 64GB ' + \
    #       str(datetime.datetime.now())
    #data = {'name': name}
    headers = {'Authorization':f'Bearer {TOKEN}','Accept': 'application/json', 'Content-Type': 'application/json'}
    resp, content = client.request(
        API_URL + '/V1/orders/items?searchCriteria=all',
        method='GET', headers=headers)
    print(resp)
    print(type(content))
    res = content.decode("utf-8")
    json_res = json.loads(res)
    with open('./integrations/magento/res.json', 'w+') as f:
        f.write(json.dumps(json_res))

if __name__ == '__main__':
    print('Session Setup:')
    print(timeit.timeit('setup()',
                        setup='from __main__ import setup',
                        number=1))
    print('Retrieving data')
    print(timeit.timeit('get_sales_data()',
                        setup='from __main__ import get_sales_data',
                        number=1))