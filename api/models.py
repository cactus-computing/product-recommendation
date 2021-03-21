from django.db import models
from django.utils import timezone
from rest_framework import serializers


# Create your models here.

class ProductAttributes(models.Model):
    '''
    Products table. This table contains all of the client's products and their atributes.
    '''
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_id = models.IntegerField(unique=True)
    sku = models.CharField(max_length=2000, default=None)
    name = models.CharField(max_length=2000)
    href = models.CharField(max_length=2000, default=None)
    permalink = models.CharField(max_length=2000)
    status = models.CharField(max_length=500)
    stock_quanity = models.FloatField(null=True, default=None)
    company = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class ModelPredictions(models.Model):
    '''
    Cross selling output. A relation of every product and the distance to every other product.
    '''
    
    product_id = models.ForeignKey(ProductAttributes, to_field="product_id", on_delete=models.CASCADE)
    recommended_id = models.ForeignKey(ProductAttributes, to_field="product_id", related_name="recommended_id", on_delete=models.CASCADE)
    distance = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.CharField(max_length=500)

    def __str__(self):
        return self.company



