from django.db import models
from django_cryptography.fields import encrypt

class Store(models.Model):
    company = models.CharField(max_length=500)
    store_logo_url = models.CharField(max_length=2000, null=True)
    gtm_id = models.CharField(max_length=500, null=True)
    ga_measurement_id = models.CharField(max_length=500, null=True)
    segment_key = models.CharField(max_length=500, null=True)
    target_div = models.CharField(max_length=500, null=True)
    product_name_selector = models.CharField(max_length=500, null=True)
    insert_before = models.CharField(max_length=500, null=True)
    product_page_identifier = models.CharField(max_length=500, null=True)
    product_page_regex = models.CharField(max_length=500, null=True)
    consumer_key = encrypt(models.CharField(max_length=500, null=True))
    consumer_secret = encrypt(models.CharField(max_length=500, null=True))
    api_url = models.CharField(max_length=1000, null=True)
    def __str__(self):
        return self.company
