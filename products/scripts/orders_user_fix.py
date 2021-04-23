from products.models import OrderAttributes
from tqdm import tqdm

def run():
    orders = OrderAttributes.objects.filter(user__icontains='k').all()
    for order in tqdm(orders):
        rut = order.user
        print(rut)
        order.user = rut.replace('k','0')
        order.save()
        print(order.user)
    orders = OrderAttributes.objects.filter(user__icontains='@').all()
    for order in tqdm(orders):
        order.user = '0'
        order.save()
        print(order.user)
    orders = OrderAttributes.objects.filter(user__icontains='K').all()
    for order in tqdm(orders):
        rut = order.user
        print(rut)
        order.user = rut.replace('K','0')
        order.save()
        print(order.user)