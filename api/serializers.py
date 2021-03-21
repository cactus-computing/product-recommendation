from rest_framework import serializers
from .models import ModelPredictions, ProductAttributes


class ModelPredictionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelPredictions
        fields = "__all__"


class ProductAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributes
        fields = "__all__"