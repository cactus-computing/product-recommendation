from rest_framework import serializers
from products.models import CrossSellPredictions, UpSellPredictions, ProductAttributes
from store.models import Front, Measurement



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
        fields = ("store_logo_url", "target_div", "product_name_selector", "target_div", "product_name_selector", "insert_before", "product_page_identifier", "product_page_regex", "button_target_div", "button_insert_before")
                

class StoreMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        depth = 1
        fields = ("store", "gtm_id", "ga_measurement_id", "segment_key")