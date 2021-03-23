from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CrossSellPredictions, UpSellPredictions, ProductAttributes
from .serializers import CrossSellPredictionsSerializer, UpSellPredictionsSerializer, ProductAttributesSerializer

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
        top_k = int(request.query_params["top-k"])
        original_product = ProductAttributes.objects.get(sku=sku, company=company)
        predictions = CrossSellPredictions.objects.filter(product_id_id=original_product.product_id, company=company)[:100]
        product_ids = list(product.recommended_id_id for product in predictions)
        predicted_products = ProductAttributes.objects.exclude(price__isnull=True).exclude(permalink__icontains="?post_type=product").filter(product_id__in=product_ids)[:top_k]
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
        top_k = int(request.query_params["top-k"])
        original_product = ProductAttributes.objects.get(sku=sku, company=company)
        predictions = UpSellPredictions.objects.filter(product_id_id=original_product.product_id, company=company)[:100]
        product_ids = list(product.recommended_id_id for product in predictions)
        predicted_products = ProductAttributes.objects.exclude(price__isnull=True).exclude(permalink__icontains="?post_type=product").filter(product_id__in=product_ids)[:top_k]
        serializer = ProductAttributesSerializer(predicted_products, many=True)
        return Response({
            "message": f"Sending top 10 up_sell predictions",
            "original_id": sku,
            "original_name": original_product.name,
            "data": serializer.data
        })