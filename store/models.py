from django.db import models
from django_cryptography.fields import encrypt

from django.db import models
from django_cryptography.fields import encrypt

class Store(models.Model):
    company = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=None, null=True)
    fare = models.IntegerField(null=True)
    
    def __str__(self):
        return self.company

class Measurement(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    gtm_id = models.CharField(max_length=500, null=True)
    ga_measurement_id = models.CharField(max_length=500, null=True)
    segment_key = models.CharField(max_length=500, null=True)

class Front(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    store_logo_url = models.CharField(max_length=2000, null=True)
    target_div = models.CharField(max_length=500, null=True)
    product_name_selector = models.CharField(max_length=500, null=True)
    insert_before = models.CharField(max_length=500, null=True)
    product_page_identifier = models.CharField(max_length=500, null=True)
    product_page_regex = models.CharField(max_length=500, null=True)

class Integration(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    api_name = models.CharField(max_length=1000, null=True)
    consumer_key = encrypt(models.CharField(max_length=500, null=True))
    consumer_secret = encrypt(models.CharField(max_length=500, null=True))
    api_url = models.CharField(max_length=1000, null=True)

class Customers(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=2000, null=True)
    last_name = models.CharField(max_length=2000, null=True)
    email = models.CharField(max_length=2000, null=True)
    accepts_marketing = models.BooleanField(default=False)
    accepts_marketing_updated_at = models.DateTimeField(auto_now_add=True)