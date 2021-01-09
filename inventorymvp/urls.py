from django.urls import path
from . import views


urlpatterns = [
    path('welcome', views.snippet_detail),
]

