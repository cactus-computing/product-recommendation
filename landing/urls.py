from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing),
]

handler404 = views.error404