from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from .scripts import woocommerce, prat, construplaza, shopify

store_type = {
    'protteina':shopify,
    'pippa':shopify,
    'amantani':shopify,
    'quema':woocommerce,
    'makerschile':woocommerce,
    'construplaza':construplaza,
    'prat':prat
}

@task(name="get_products")
def get_products(store):
    store_type[store].get_products(store)

@task(name="get_orders")
def get_orders(store):
    store_type[store].get_orders(store)
        