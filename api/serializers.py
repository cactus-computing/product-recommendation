from rest_framework import serializers
from products.models import CrossSellPredictions, UpSellPredictions, ProductAttributes
from store.models import Store



class CrossSellPredictionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrossSellPredictions
        fields = "__all__"

class UpSellPredictionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpSellPredictions
        fields = "__all__"

class ProductAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributes
        fields = "__all__"

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ("company", "store_logo_url", "gtm_id", "ga_measurement_id", "target_div", "product_name_selector", "insert_before", "product_page_identifier", "product_page_regex")