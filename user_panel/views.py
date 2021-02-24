from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as do_logout
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FieldSelectionForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .forms import FileSubmissionForm, FieldSelectionForm
from .models import CompanyData, handle_uploaded_file, get_available_fields, rename_dataset
import logging
from django.core.mail import send_mail, send_mass_mail
from django.template import Context, loader


from .models import User, Company
from .storage import rename_dataset

class Welcome(LoginRequiredMixin, View):
    def get(self, request):
        form = FileSubmissionForm
        return render(request, 'welcome.html', { 'form':form })
    
    def post(self, request):
        form = FileSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            file_path, gc_url = handle_uploaded_file(request.FILES['document'], company=request.user.company, local=False)
            stored_file = Company(document_location=file_path, user=request.user)
            stored_file.save()
            email_cliente = f"""Hola, {request.user.first_name}!\n\nTu data está siendo procesada y te enviarémos un correo a penas tengamos el resultado.\n\nGracias por confiar en nosotros!\n\nEquipo de Cactus Co"""
            email_interno = f"""Nueva data subida por {request.user.first_name} {request.user.last_name} de {request.user.company}, este es el archivo {file_path}"""
            
            message1 = (
                'Recomendacion de productos',
                email_cliente,  
                'agustin.escobar@cactusco.cl', 
                [email]
            )
            message2 = (
                f'Nueva data!! Cliente: {request.user.first_name} {request.user.last_name}, {request.user.company}',
                email_interno, 
                'agustin.escobar@cactusco.cl', 
                ['agustin@cactusco.cl', 'vicente@cactusco.cl', 'rodrigo@cactusco.cl']
            )

            send_mass_mail((message1, message2), fail_silently=False)

            request.session['file_path'] = file_path
            request.session['available_fields'] = get_available_fields(file_path)
            return HttpResponseRedirect(reverse('field-selection'), { "has_submitted": False })
        return render(request, 'welcome.html', { 'form':form })

class FieldSelection(LoginRequiredMixin, View):
    available_fields = [
        ('Fecha', 'Date'), 
        ('Número de boleta', 'Bill Number'),
        ('ID de Usuario', 'User ID'),
        ('Código de producto (SKU)', 'SKU'),
        ('Cantidad de productos', 'Quant'), 
        ('Descripción del producto', 'Description')
    ]

    def post(self, request):
        '''
        Parameters:
            - request: request.POST contains the form data
        Returns:
            - renders the field selection form to rename the uploaded dataframes or if handled correctly
            it redirects to the Landing Page
        '''

        if 'available_fields' in request.session:
            self.available_fields = []
            for key in request.session['available_fields']:
                self.available_fields.append((key, key))

        form = FieldSelectionForm(self.available_fields, request.POST)

        if form.is_valid():
            rename_dataset(request.session['file_path'], form.cleaned_data)
            return render(request, 'sections/welcome.html', { 'has_submitted': True,  'no_user': True })

        form = FieldSelectionForm(available_fields=self.available_fields)

        return render(request, 'forms/field_selection.html', { 'form':form })
