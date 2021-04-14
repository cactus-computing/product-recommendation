from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing, name='landing'),
    path('thanks/contact', views.thanks_contact, name='thanks_contact'),
    path('thanks/suscription', views.thanks_suscription, name='thanks_suscription'),
    path('demos', views.Demos.as_view(), name='demos'),
    path('demos/landing', views.Demos.as_view(), name='landing')
]

handler404 = views.error404