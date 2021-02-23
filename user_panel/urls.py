from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProtectView.as_view(), name='user-welcome'),
]