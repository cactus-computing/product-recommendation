from rest_framework import serializers
from products.models import CrossSellPredictions, UpSellPredictions, ProductAttributes
from store.models import Front, Integration



class CrossSellPredictionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrossSellPredictions
        depth = 1
        fields = ("id", "distance", "recommended_code")

class UpSellPredictionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpSellPredictions
        depth = 1
        fields = ("id", "distance", "recommended_code")

class ProductAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributes
        fields = "__all__"

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Front
        depth = 1
        fields = ("company", "front", "Integration")

class StoreFrontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Front
        depth = 1
        fields = ("store_logo_url", "target_div", "product_name_selector", "target_div", "product_name_selector", "insert_before", "product_page_identifier", "product_page_regex")
                
class StoreIntegrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integration
        depth = 1
        fields = ("api_name", "consumer_key", "consumer_secret", "api_url")