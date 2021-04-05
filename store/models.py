from django.db import models
from django_cryptography.fields import encrypt

class Store(models.Model):
    company = models.CharField(max_length=500)
    gtm_id = models.CharField(max_length=500)
    ga_measurement_id = models.CharField(max_length=500)
    segment_key = models.CharField(max_length=500)
    target_div = models.CharField(max_length=500)
    product_name_selector = models.CharField(max_length=500)
    insert_before = models.CharField(max_length=500)
    product_page_identifier = models.CharField(max_length=500)
    product_page_regex = models.CharField(max_length=500)
    consumer_key = encrypt(models.CharField(max_length=500, null=True))
    consumer_secret = encrypt(models.CharField(max_length=500, null=True))
    api_url = models.CharField(max_length=1000, null=True)
    def __str__(self):
        return self.company
