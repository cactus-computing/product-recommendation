from django.urls import path
from . import views


urlpatterns = [
    path('test', views.testing_api, name="api_test"),
    path('cross_selling', views.cross_selling, name="cross_selling"),
    path('up_selling', views.up_selling, name="up_selling"),
    path('random_product', views.random_product_for_client, name="random_product"),
    path('update_price_and_stock', views.update_price_and_stock, name="update_price_and_stock"),
    path('store/front_info', views.GetStoreFrontDetails.as_view(), name="store_front_info"),
    path('store/analytics_info', views.GetStoreAnalytics.as_view(), name="store_analytics_info"),
    path('get_product_info', views.ProductInfo.as_view(), name="get_product_info"),
]