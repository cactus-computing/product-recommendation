from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
from products.models import CrossSellPredictions, UpSellPredictions, ProductAttributes
from .serializers import CrossSellPredictionsSerializer, UpSellPredictionsSerializer, ProductAttributesSerializer


def point_to_int(price):
    price = int(price.split('.')[0])
    price = f"${price:,}".replace(',','.')
    return price

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
        name = request.query_params["name"].strip().lower()
        company = request.query_params["company"]
        top_k = int(request.query_params["top-k"])
        original_product = ProductAttributes.objects.filter(name__iexact=name, company__company=company).first()
        if original_product is None:
            return Response({
                "message": "Your product was not found :(",
                "error": True,
                "empty": True,
            })
        predictions = CrossSellPredictions.objects.filter(product_code__name__iexact=name, company__company=company)
        predictions = predictions.exclude(product_code__price__isnull=True, product_code__stock_quantity=False)
        predictions = predictions.order_by('-distance')
        product_ids = list(product.recommended_code_id for product in predictions)
        predicted_products = ProductAttributes.objects.exclude(price__isnull=True, product_code__stock_quantity=False).filter(id__in=product_ids)[:top_k]
        serializer = ProductAttributesSerializer(predicted_products, many=True)
        for obj in  serializer.data:
            obj["price"] = point_to_int(obj["price"])

        return Response({
            "message": f"Sending top 10 cross_sell predictions",
            "query_name": name,
            "original_name": original_product.name,
            "original_code": original_product.product_code,
            "empty": len(serializer.data) == 0,
            "data": serializer.data
        })

@api_view(['GET', 'POST'])
def up_selling(request):
    '''
    Given a sku and company get up_sell skus
    '''

    if request.method == "GET":
        name = request.query_params["name"].strip().lower()
        company = request.query_params["company"]
        top_k = int(request.query_params["top-k"])
        original_product = ProductAttributes.objects.filter(name__iexact=name, company__company=company).first()
        if original_product is None:
            return Response({
                "message": "Your product was not found :(",
                "error": True,
                "empty": True,
            })

        predictions = UpSellPredictions.objects.filter(product_code__name__iexact=name, company__company=company)
        predictions = predictions.exclude(product_code__price__isnull=True, product_code__stock_quantity=False)
        predictions = predictions.order_by('-distance')
        product_ids = list(product.recommended_code_id for product in predictions)
        predicted_products = ProductAttributes.objects.exclude(price__isnull=True, product_code__stock_quantity=False).filter(id__in=product_ids)[:top_k]
        serializer = ProductAttributesSerializer(predicted_products, many=True)
        for obj in  serializer.data:
            obj["price"] = point_to_int(obj["price"])
            
        return Response({
            "message": "Sending top 10 Up Selling predictions",
            "query_name": name,
            "original_name": original_product.name,
            "original_code": original_product.product_code,
            "empty": len(serializer.data) == 0,
            "data": serializer.data
        })

@api_view(['GET', 'POST'])
def random_product_for_client(request):
    '''
    Given a sku and company get up_sell skus
    '''

    if request.method == "GET":
        company_name = request.query_params["company"]
        products_count = ProductAttributes.objects.filter(company__company=company_name).count()
        
        rand_int = random.randint(0, products_count-1)
        products_objects = ProductAttributes.objects.filter(company__company=company_name)[rand_int]
        serializer = ProductAttributesSerializer(products_objects)
        return Response({
            "message": "Selecting random product",
            "products_count": products_count,
            "selected_product": serializer.data
        })

@api_view(['POST'])
def update_price_and_stock(request):
    '''
    Updates the price and stock availability of a give product
    '''

    if request.method == "POST":
        product_name = request.data.get("product_name")
        company = request.data.get("company")
        price = request.data.get("price")
        stock = request.data.get("stock")

        try: 
            producto = ProductAttributes.objects.filter(name__iexact=product_name, company__company=company)
        except ProductAttributes.DoesNotExist:
            return Response({
                "error": f"Product {product_name} was not found"
            })

        producto.update(price=price, stock_quantity=stock)

        return Response({
            "message": "Updated price and stock",
            "price": price,
            "stock": stock
        })