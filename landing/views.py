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
            "similar_products": [
                { "name": "RODILLO TEXTURAR 7 Pul. 18 CMS. LIZCAL", "score": 0.9659267, "img_name": 'img/rodillo_lana.png'  },
                { "name": "RODILLO ESPONJA 7 Pul. 18 CMS. LIZCAL", "score": 0.9403552, "img_name": 'img/rodillo_microfibra.png'  },
                { "name": "RODILLO CHIPORRO 9 Pul. 24 CMS. LIZCAL", "score": 0.8460233, "img_name": 'img/rodillo_texturador.png'  }
            ],
            "related_products": [
                { "name": "RODILLO CHIPORRO 4 Pul. 9 CMS LIZCAL", "score": 0.81059957, "img_name": 'img/cinta_enmascarar.png'  },
                { "name": "RODILLO ESPONJA 3 Pul. 7 CMS. LIZCAL", "score": 0.79706407, "img_name": 'img/pasta_interior.png'  },
                { "name": "RODILLO CHIPORRO 5 Pul. 12 CMS. LIZCAL", "score": 0.79489124, "img_name": 'img/adhesivo.png'  }
            ]
        },
        {
            "code": "14853610",
            "img_name": "img/14853610.png",
            "name": "React Infinity Run 2 Zapatilla Running Mujer",
            "similar_products": [
                { "name": "React Infinity Run Zapatilla Running Mujer", "score": 0.98, "img_name": 'img/zapatillas1.png' },
                { "name": "Run Swift 2 Zapatilla Running Mujer", "score": 0.95, "img_name": 'img/zapatillas2.png' },
                { "name": "Renew Run 2 Zapatilla Running Mujer", "score": 0.83, "img_name": 'img/zapatillas3.png' },
            ],
            "related_products": [
                { "name": "Polerón Deportivo Hombre", "score": 0.87, "img_name": 'img/poleron-png.jfif' },
                { "name": "Bolso deportivo 60L", "score": 0.84, "img_name": 'img/Bolso.png' },
                { "name": "Calcetines deportivos", "score": 0.77, "img_name": 'img/Calcetines.png' }
            ]
        },
        {
            "code": "6816177",
            "img_name": "img/refri.png",
            "name": "Refrigerador Midea MRFI-1800 180 L",
            "similar_products": [
                { "name": "Refrigerador Bottom Freezer No Frost 290 lt RMB302PXLRS0", "score": 0.99, "img_name": "img/refri2.png"},
                { "name": "Refrigerador Frío Directo 207 lt MRFS-2100S273FN", "score": 0.92, "img_name": "img/refri3.png" },
                { "name": "Refrigerador Frío Directo 205 lt RD-2000SI", "score": 0.83, "img_name": "img/refri4.png" }
            ],
            "related_products": [
                { "name": "Humidificador Difusor De Aroma Ultrasónico X1", "score": 0.89, "img_name": "img/humi.png" },
                { "name": "@FREEZER H SINDELEN SFH-150BL 150LT", "score": 0.86, "img_name": "img/freezer.png" },
                { "name": "Cocina a Gas 4 Quemadores Andes60TX3", "score": 0.81, "img_name": "img/cocina.png" }
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