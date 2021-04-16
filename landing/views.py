from rest_framework.views import APIView
from rest_framework.response import Response
from .forms import ContactForm
from .serializers import ContactSerializer
import logging
from django.core.mail import EmailMessage, send_mass_mail


logger = logging.Logger(__name__)

class HandleContactData(APIView):
    '''
    Details the product attributes
    '''
    def post(self, request, format=None):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            email = serializer.data['email']
            name = serializer.data['name']
            phone = serializer.data['phone']
            website = serializer.data['website']

            client_message = f"""Hola, {name}!\n\n¡Gracias por contactarte con nosotros! Nuestro equipo se contactará contigo antes de 24 horas."""
            internal_message = f"""Datos del nuevo contacto:\n\nNombre:{name}\n\nEmail: {email}\n\nTelefono: {phone}\n\nURL:{website}"""
            
            client_mail = (
                '[Cactus Co] Bienvenida', #subject 
                client_message,  #message
                'agustin@cactusco.cl', # from
                [email] # to
            )

            internal_mail = (
                f'Contacto en CactusCo.cl',
                internal_message,
                'contacto@cactusco.cl',
                ['agustin@cactusco.cl', 'vicente@cactusco.cl', 'rodrigo@cactusco.cl']
            )
            
            send_mass_mail((client_mail, internal_mail), fail_silently=False)

            submitted = True

            return Response(serializer.data)  
        return Response({'errors': serializer.errors})
