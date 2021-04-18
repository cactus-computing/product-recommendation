from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
import random
import json
from products.models import CrossSellPredictions, UpSellPredictions, Products
from store.models import Store
from .serializers import StoreSerializer
from .serializers import CrossSellPredictionsSerializer, UpSellPredictionsSerializer, ProductAttributesSerializer


def format_price(price):
    if price is not None:
        price = int(price.split('.')[0])
        price = f"${price:,}".replace(',','.')
        return price
    else:
        return None
    

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
        original_product = ProductAttributes.objects.filter(
            name__iexact=name, 
            company__company=company).prefetch_related("crosssellpredictions_set").first()
        # indice al nombre y por distance
        if original_product is None:
            return Response({
                "message": "Your product was not found :(",
                "error": True,
                "empty": True,
            })
        predictions = original_product.crosssellpredictions_set.prefetch_related('recommended_code')
        predictions = predictions.filter(
            recommended_code__price__isnull=False,
            recommended_code__stock_quantity=True,
            recommended_code__status=True,
        )
        predictions = predictions.select_related('recommended_code').order_by('-distance')[:top_k]

        serializer = CrossSellPredictionsSerializer(predictions, many=True)
        for obj in  serializer.data:
            obj["recommended_code"]["price"] = format_price(obj["recommended_code"]["price"])
            obj["recommended_code"]["compare_at_price"] = format_price(obj["recommended_code"]["compare_at_price"])

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
        original_product = ProductAttributes.objects.filter(
            name__iexact=name, 
            company__company=company).prefetch_related("upsellpredictions_set").first()
        if original_product is None:
            return Response({
                "message": "Your product was not found :(",
                "error": True,
                "empty": True,
            })

        predictions = original_product.upsellpredictions_set.prefetch_related('recommended_code')
        predictions = predictions.filter(
            recommended_code__price__isnull=False,
            recommended_code__stock_quantity=True,
            recommended_code__status=True,
        )
        predictions = predictions.select_related('recommended_code').order_by('-distance')[:top_k]

        serializer = UpSellPredictionsSerializer(predictions, many=True)
        for obj in  serializer.data:
            obj["recommended_code"]["price"] = format_price(obj["recommended_code"]["price"])
            obj["recommended_code"]["compare_at_price"] = format_price(obj["recommended_code"]["compare_at_price"])
            
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
        product = serializer.data.copy()
        product['formatted_price'] = format_price(product['price'])
        return Response({
            "message": "Selecting random product",
            "products_count": products_count,
            "selected_product": product
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

@api_view(['GET'])
def get_store_details(request):
    '''
    Updates the price and stock availability of a give product
    '''

    if request.method == "GET":
        company = request.query_params.get("company")
        print(company)
        try: 
            store = Store.objects.filter(company=company).first()
        except Store.DoesNotExist:
            return Response({
                "error": f"Product {company} was not found"
            })
        store_serializer = StoreSerializer(store)
        return Response({
            "message": "Store successfully retrieved",
            "store_data": store_serializer.data
        })

class ProductInfo(APIView):
    '''
    Details the product attributes
    '''
    def get(self, request, format=None):
        product_names = json.loads(request.query_params.get("products"))
        company = request.query_params.get("company")
        product_objects = set()
        errors = []
        for product_name in product_names:
            try:
                product = ProductAttributes.objects.filter(
                    name__iexact=product_name, 
                    company__company=company).first()
                if product is not None:
                    product_objects.add(product)
            except ProductAttributes.DoesNotExist:
                errors.append(f"The following products from {company} where not found: {', '.join(product_name)}")

        product_serializer = ProductAttributesSerializer(product_objects, many=True)

        for obj in  product_serializer.data:
            obj["price"] = format_price(obj["price"])
            obj["compare_at_price"] = format_price(obj["compare_at_price"])

        res = {}
        res['data'] = product_serializer.data
        res['errors'] = errors
        return Response(res)

