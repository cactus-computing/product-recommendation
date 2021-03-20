from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ModelPredictions

def get_top_predictions_for(porduct_id, k=5):
    return ModelPredictions.objects.filter(porduct_id=product_id)[:k]

products = [
    {
        "sku": 3494551,
        "price": 2590,
        "name": "Rodillo chiporro",
        "href": "https://sodimac.scene7.com/is/image/SodimacCL/3494551?fmt=jpg&fit=constrain,1&wid=420&hei=420"
    },
    {
        "sku": 1954210,
        "price": 9990,
        "name": "Pistola de silicona",
        "href": "https://sodimac.scene7.com/is/image/SodimacCL/1954210?fmt=jpg&fit=constrain,1&wid=420&hei=420"
    },
    {
        "sku": 8700575,
        "price": 129990,
        "name": "Taladro",
        "href": "https://sodimac.scene7.com/is/image/SodimacCL/8700575?fmt=jpg&fit=constrain,1&wid=420&hei=420"
    },
]

@api_view(['GET', 'POST'])
def testing_api(request):
    '''
    General testing
    '''
    if request.method == "GET":
        return Response({
            "message": "you sent a get request",
            "data": products
        })