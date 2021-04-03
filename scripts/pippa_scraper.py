import pandas as pd
from tqdm import tqdm
import requests as req
from bs4 import BeautifulSoup
from store.models import Store
from products.models import ProductAttributes

def pippa_product_price(html):
    price = html.find('span', {'itemprop': 'price'}).text.strip().replace('$', '').replace('.', '')
    return int(price)

def pippa_has_stock(html):
    stock = False if html.find('span', {'class': 'sold_out'}).text.strip().replace('$', '').replace('.', '') is not None else True
    return stock

def pippa_image_link(html):
    return html.find('div', {"class": "product_gallery"}).find('img').get('data-src').strip()

def run(*args):
    r = req.get("https://www.pippa.cl/sitemap_products_1.xml?from=2065737842753&to=6543288336449")
    soup = BeautifulSoup(r.text)
    company = Store.objects.get(company='pippa')
    for e, product in enumerate(tqdm(soup.find_all('url'))):
        res = req.get(product.find('loc').text)
        product_html = BeautifulSoup(res.text)
        if e == 0:
            continue
        try:
            ProductAttributes.objects.update_or_create(
                name=product.find('image:title').text,
                permalink=product.find('loc').text,
                company=company,
                defaults={
                    'product_code': e-1,
                    'sku': e-1,
                    'img_url': pippa_image_link(product_html),
                    'stock_quantity': pippa_has_stock(product_html),
                    'status': 'Published',
                    'price': pippa_product_price(product_html),
                    'record_created_at': product.find('lastmod').text
                }
            )
        except IntegrityError as f:
            logger.error(f)
            continue