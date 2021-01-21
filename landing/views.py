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

    return render(request, 'landing.html', { 'contactForm': contactForm, 'suscriptionForm': suscriptionForm, 'countDownDateTime': datetime.datetime.now() })   

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