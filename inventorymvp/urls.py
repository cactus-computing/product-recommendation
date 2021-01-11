from django.urls import path
from . import views


urlpatterns = [
    path('welcome', views.main_form),
    path('field_selection', views.field_selection, name='field-selection'),
]

