from django.contrib import admin
from .models import Store, Customers

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    model = Store

from .models import Measurement, Front, Integration

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class MeasurementInline(admin.StackedInline):
    model = Measurement
    can_delete = False

class FrontInline(admin.StackedInline):
    model = Front
    can_delete = False

class IntegrationInline(admin.StackedInline):
    model = Integration
    can_delete = False

# Define a new User admin
class StoreAdmin(StoreAdmin):
    inlines = (MeasurementInline,FrontInline,IntegrationInline,)

# Re-register UserAdmin
admin.site.unregister(Store)
admin.site.register(Store, StoreAdmin)
admin.site.register(Customers)