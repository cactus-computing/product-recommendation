from django.contrib import admin
from .models import ProductAttributes, OrderAttributes, CrossSellPredictions, UpSellPredictions

admin.site.register(OrderAttributes)
admin.site.register(ProductAttributes)
admin.site.register(CrossSellPredictions)
admin.site.register(UpSellPredictions)