from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Welcome.as_view(), name='user-welcome'),
    path('field_selection', views.FieldSelection.as_view(), name='field-selection'),
]