from django.urls import path
from . import views


urlpatterns = [
    path('contact', views.HandleContactData.as_view(), name='landing'),
]