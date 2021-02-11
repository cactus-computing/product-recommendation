from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing, name='landing'),
    path('thanks/contact', views.thanks_contact),
    path('thanks/suscription', views.thanks_suscription),
]

handler404 = views.error404