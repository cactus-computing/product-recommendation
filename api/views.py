from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ModelPredictions, ProductAttributes
from .serializers import ModelPredictionsSerializer, ProductAttributesSerializer

def get_top_predictions_for(porduct_id, k=5):
    return ModelPredictions.objects.filter(porduct_id=product_id)[:k]

@api_view(['GET', 'POST'])
def testing_api(request):
    '''
    General testing of some products
    '''
    products = ProductAttributes.objects.all()
    serializer = ProductAttributesSerializer(products, many=True)
    if request.method == "GET":
        return Response({'data': serializer.data})

@api_view(['GET', 'POST'])
def cross_selling(request):
    '''
    General testing
    '''
    sku = request.query_params["sku"]
    company = request.query_params["company"]
    predictions = ModelPredictions.objects.filter(product_id_id=sku, company=company)[:10]
    original_product = ProductAttributes.objects.get(product_id=sku, company=company)
    product_ids = list(product.recommended_id_id for product in predictions)
    predicted_products = ProductAttributes.objects.filter(product_id__in=product_ids)
    serializer = ProductAttributesSerializer(predicted_products, many=True)
    if request.method == "GET":
        return Response({
            "message": f"Sending top 10 predictions",
            "original_id": sku,
            "original_name": original_product.name,
            "data": serializer.data
        })