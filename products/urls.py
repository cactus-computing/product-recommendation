from django.urls import path
from . import views


urlpatterns = [
    path('get_products',  views.GetProductsInfo.as_view(), name="get_products"),
    path('get_orders',  views.GetOrdersInfo.as_view(), name="get_orders"),
    path('check_status',  views.CheckTaskStatus.as_view(), name="check_status"),
]