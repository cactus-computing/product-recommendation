from django.db import models
from rest_framework import serializers


# Create your models here.

class ProductAttributes(models.Model):
    '''
    User Model. The user of our application.
    '''

    product_id = models.IntegerField(unique=True)
    sku = models.CharField(max_length=2000, default=None)
    name = models.CharField(max_length=2000)
    href = models.CharField(max_length=2000, default=None)
    company = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class ModelPredictions(models.Model):
    '''
    User Model. The user of our application.
    '''
    
    product_id = models.ForeignKey(ProductAttributes, to_field="product_id", on_delete=models.CASCADE)
    recommended_id = models.ForeignKey(ProductAttributes, to_field="product_id", related_name="recommended_id", on_delete=models.CASCADE)
    distance = models.FloatField()
    created_at = models.DateTimeField()
    company = models.CharField(max_length=500)

    def __str__(self):
        return self.company



