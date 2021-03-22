from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CrossSellPredictions, UpSellPredictions, ProductAttributes
from .serializers import CrossSellPredictionsSerializer, UpSellPredictionsSerializer

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
    Given a sku and company get cross_sell skus
    '''
    if request.method == "GET":
        sku = request.query_params["sku"]
        company = request.query_params["company"]
        predictions = CrossSellPredictions.objects.filter(product_id_id=sku, company=company)[:10]
        original_product = ProductAttributes.objects.get(product_id=sku, company=company)
        product_ids = list(product.recommended_id_id for product in predictions)
        predicted_products = ProductAttributes.objects.filter(product_id__in=product_ids)
        serializer = ProductAttributesSerializer(predicted_products, many=True)
        return Response({
            "message": f"Sending top 10 cross_sell predictions",
            "original_id": sku,
            "original_name": original_product.name,
            "data": serializer.data
        })

@api_view(['GET', 'POST'])
def up_selling(request):
    '''
    Given a sku and company get up_sell skus
    '''
    if request.method == "GET":
        sku = request.query_params["sku"]
        company = request.query_params["company"]
        predictions = UpSellPredictions.objects.filter(product_id_id=sku, company=company)[:10]
        original_product = ProductAttributes.objects.get(product_id=sku, company=company)
        product_ids = list(product.recommended_id_id for product in predictions)
        predicted_products = ProductAttributes.objects.filter(product_id__in=product_ids)
        serializer = ProductAttributesSerializer(predicted_products, many=True)
        return Response({
            "message": f"Sending top 10 up_sell predictions",
            "original_id": sku,
            "original_name": original_product.name,
            "data": serializer.data
        })