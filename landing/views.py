from django.shortcuts import render, redirect, get_object_or_404
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.db import utils
from .forms import ContactForm, SuscriptionForm
from .models import Suscription
import logging
from django.core.mail import EmailMessage, send_mass_mail
from django.urls import reverse
from django.template import Context, loader

logger = logging.Logger(__name__)
recommended_products = [
        {
            "code": "ROD013373",
            "img_name": "img/ROD013373.png",
            "name": "RODILLO CHIPORRO 7 Pul. 18 CMS. LIZCAL",
            "recommended": [
                { "name": "RODILLO TEXTURAR 7 Pul. 18 CMS. LIZCAL", "score": 0.9659267 },
                { "name": "RODILLO ESPONJA 7 Pul. 18 CMS. LIZCAL", "score": 0.9403552 },
                { "name": "RODILLO CHIPORRO 9 Pul. 24 CMS. LIZCAL", "score": 0.8460233 },
                { "name": "RODILLO CHIPORRO 4 Pul. 9 CMS LIZCAL", "score": 0.81059957 },
                { "name": "RODILLO ESPONJA 3 Pul. 7 CMS. LIZCAL", "score": 0.79706407 },
                { "name": "RODILLO CHIPORRO 5 Pul. 12 CMS. LIZCAL", "score": 0.79489124 },
                { "name": "RODILLO ESPONJA 1 1/2 Pul. 4.5 CMS. LIZCAL", "score": 0.78571963 },
                { "name": "RODILLO ESPONJA 5 Pul. 12 CMS. LIZCAL", "score": 0.7753909 }
            ]
        },
        {
            "code": "PAS119006",
            "img_name": "img/PAS119006.jpeg",
            "name": "PASTA MURO TAJAMAR F-15 25 KGS",
            "recommended": [
                { "name": "PASTA MURO TAJAMAR F-15 30 KGS", "score": 0.9304087 },
                { "name": "PASTA MURO TAJAMAR F-15 1/2 TINETA", "score": 0.82496035 },
                { "name": "SOQUINA PASTA MURO 1KG", "score": 0.6861458 },
                { "name": "PASTA ESMERIL PULIR 250 GRAMOS GRANO N° 100", "score": 0.6724293 },
                { "name": "ADHESIVO PASTA CADINA AC BALDE 25 KG", "score": 0.6693083 },
                { "name": "TAJAMAR PASTA MURO SUPER F-6 1KG", "score": 0.6657156 },
                { "name": "CERESITA PASTA MURO 1KG", "score": 0.6600415 },
                { "name": "PASTA ESMERIL PULIR 250 GRAMOS GRANO N° 120", "score": 0.65710866 }
            ]
        },
        {
            "code": "TER018624",
            "img_name": "img/TER018624.jpg",
            "name": "TERCIADO ESTRUCTURAL 15 MM 1220 X 2440",
            "recommended": [
                { "name": "TERCIADO MOLDAJE 15 MM 1220 X 2440", "score": 0.95978415 },
                { "name": "TERCIADO ESTRUCTURAL 18 MM 1220 X 2440", "score": 0.8745111 },
                { "name": "TERCIADO MOLDAJE 18 MM 1220 X 2440", "score": 0.8411093 },
                { "name": "TERCIADO ESTRUCTURAL 12 MM 1220 X 2440", "score": 0.8237744 },
                { "name": "MASISA MELAMINA LINGUE 15 X 1520 X 2440", "score": 0.7271608 },
                { "name": "MASISA MELAMINA LENGA 15 X 1520 X 2440", "score": 0.72601295 },
                { "name": "DUROLAC 3 MM COIGUE 1520 X 2440", "score": 0.7090162 },
                { "name": "DUROLAC 3 MM CEDRO 1520 X 2440", "score": 0.7078656 }
            ]
        }
    ]
def landing(request):
    '''
    Main function for handling landing page operations and form submission.
    Parameters:
        - request: contains the details of the user email in the .POST attribute.
    Returns:
        - conditional to program flow: renders the landing page or redirects to the field selection form (field_selection function).
    '''

    contactForm = ContactForm
    suscriptionForm = SuscriptionForm
    
    return render(request, 'landing.html', { 'contactForm': contactForm, 'suscriptionForm': suscriptionForm, 'countDownDateTime': datetime.datetime.now(), 'recommendedProducts': recommended_products })   

def thanks_suscription(request):
    if request.method == "POST":
        suscriptionForm = SuscriptionForm(request.POST)
        if suscriptionForm.is_valid():
            
            email = suscriptionForm.cleaned_data['email']

            suscription = Suscription(email=email)
            
            try:
                suscription.save()
            except utils.IntegrityError:
                suscription = Suscription.objects.get(email=suscription)

            client_message = f"""Hola, {email}!\n\n¡Ya estas en nuestros registros!.\n\nTe enviaremos información y actualizaciones sobre los avances de nuestro producto directamente a tu mail."""

            client_mail = (
                'Bienvenido a CactusCo',
                client_message,
                'contacto@cactusco.cl',
                [email]
            )
                
            internal_message = f"""Datos de la suscripcioón:\n\nEmail: {email}\n\nFecha de creación: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"""
            internal_mail = (
                f'Contacto en CactusCo.cl',
                internal_message,
                'contacto@cactusco.cl',
                ['agustin.escobar@cactusco.cl', 'vicente.escobar@cactusco.cl', 'rodrigo.oyarzun25@gmail.com']
            )

            
            send_mass_mail((client_mail, internal_mail), fail_silently=False)

    return render(request, 'thanks.html', {'message': '¡Gracias por suscribirte!'})

def thanks_contact(request):
    submitted = False
    if request.method == "POST":
        
        contactForm = ContactForm(request.POST)
        if contactForm.is_valid():
            email = contactForm.cleaned_data['email']
            name = contactForm.cleaned_data['name']
            phone = contactForm.cleaned_data['phone']
            message = contactForm.cleaned_data['message']
            
            client_message = f"""Hola, {name}!\n\n¡Gracias por contactarte con nosotros! Nuestro equipo se contactará contigo antes de 24 horas."""
            internal_message = f"""Datos del nuevo contacto:\n\nNombre:{name}\n\nEmail: {email}\n\nEmail: {phone}"""
            
            client_mail = (
                '[Cactus Co] Bienvenida', #subject 
                client_message,  #message
                'agustin.escobar@cactusco.cl', # from
                [email] # to
            )

            internal_mail = (
                f'Contacto en CactusCo.cl',
                internal_message,
                'contacto@cactusco.cl',
                ['agustin.escobar@cactusco.cl', 'vicente.escobar@cactusco.cl', 'rodrigo.oyarzun25@gmail.com']
            )
            
            send_mass_mail((client_mail, internal_mail), fail_silently=False)

            submitted = True
    return render(request, 'thanks.html', {'message': '¡Gracias por tu contacto!'})

def error404(request, exception):
    template = loader.get_template('404.html')
    context = Context({
        'message': 'All: %s' % request,
        })
    return HttpResponse(content=template.render(context), content_type='text/html; charset=utf-8', status=404) 