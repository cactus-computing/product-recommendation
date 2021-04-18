from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.decorators import task

@task(name="sum_two_numbers")
def add(x, y):
    print("Hello World")
    return x + y

from .scripts.wc_get_products import wc_products

@task(name="wc_get_products")
def wc_products_get():
    wc_products()

from .scripts.shopify import shopify_funct

@task(name="shopify")
def shopify():
    stores = ['protteina', 'pippa', 'amantani']
    for store in stores:
        shopify_funct(store)
        
from .scripts.prat_get_products import run

@task(name="prat_get_products")
def prat_get_products():
    run()

from .scripts.scraper_construplaza import constru_get_products

@task(name="construplaza_get_products")
def construplaza_get_products():
    constru_get_products()
