from django.urls import path
from . import views


urlpatterns = [
    path('test', views.testing_api, name="api_test"),
    path('cross_selling', views.cross_selling, name="cross_selling"),
    path('up_selling', views.up_selling, name="up_selling"),
    path('random_product', views.random_product_for_client, name="random_product")
]

#handler404 = views.error404