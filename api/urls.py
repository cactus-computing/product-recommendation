from django.urls import path
from . import views


urlpatterns = [
    path('test', views.testing_api, name="api_test"),
    path('cross_selling', views.cross_selling, name="cross_selling"),
    path('up_selling', views.up_selling, name="up_selling"),
<<<<<<< HEAD
    path('random_product', views.random_product_for_client, name="random_product")
=======
    path('update_price_and_stock', views.update_price_and_stock, name="update_price_and_stock")
>>>>>>> f05bad4 (feat(api): adds update_price_stock endpoint and updates cross and upselling filters)
]

#handler404 = views.error404