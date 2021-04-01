from rest_framework import serializers
from products.models import CrossSellPredictions, UpSellPredictions, ProductAttributes


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