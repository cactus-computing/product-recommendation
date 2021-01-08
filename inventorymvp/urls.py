from django.urls import path
from . import views


urlpatterns = [
    path('form', views.snippet_detail),
]

