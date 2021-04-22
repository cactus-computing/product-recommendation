from django.contrib import admin
from .models import Store, Measurement, Front, Integration, Customers

admin.site.register(Store)
admin.site.register(Measurement)
admin.site.register(Front)
admin.site.register(Integration)
admin.site.register(Customers)