from products.models import ProductAttributes
from store.models import Store

def run():

    objects = ProductAttributes.objects.filter(company_id=4, permalink__contains="www.").delete()
    print(objects)