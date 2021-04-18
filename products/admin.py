from django.contrib import admin
from .models import Products, Orders, CrossSellPredictions, UpSellPredictions

admin.site.register(Orders)
admin.site.register(Products)
admin.site.register(CrossSellPredictions)
admin.site.register(UpSellPredictions)