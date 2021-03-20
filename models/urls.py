from django.urls import path
from . import views


urlpatterns = [
    path('test', views.testing_api, name="api_test")
]

#handler404 = views.error404