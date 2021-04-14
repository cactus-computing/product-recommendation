from django.urls import path
from . import views


urlpatterns = [
    path('', views.Demos.as_view(), name='landing'),
    path('thanks/contact', views.thanks_contact, name='thanks_contact'),
    path('thanks/suscription', views.thanks_suscription, name='thanks_suscription'),
]

handler404 = views.error404