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
from .models import User, Company, CompanyData
import logging
from django.core.mail import send_mail, send_mass_mail
from django.template import Context, loader

from .storage import rename_dataset, handle_uploaded_file, get_available_fields

class Welcome(LoginRequiredMixin, View):
    available_fields = [
        ('Fecha', 'Date'), 
        ('Número de boleta', 'Bill Number'),
        ('ID de Usuario', 'User ID'),
        ('Código de producto (SKU)', 'SKU'),
        ('Cantidad de productos', 'Quant'), 
        ('Descripción del producto', 'Description')
    ]

    def get(self, request):
        form = FileSubmissionForm
        return render(request, 'welcome.html', { 'form':form })
    
    def post(self, request):
        form = FileSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            company = get_object_or_404(Company, user=request.user)
            file_path, gc_url = handle_uploaded_file(request.FILES['document'], company=company.Company, local=False)
            stored_file = CompanyData(document_location=file_path, owner=request.user)
            stored_file.save()
            email_cliente = f"""Hola, {request.user.first_name}!\n\nTu data está siendo procesada y te enviarémos un correo a penas tengamos el resultado.\n\nGracias por confiar en nosotros!\n\nEquipo de Cactus Co"""
            email_interno = f"""Nueva data subida por {request.user.first_name} {request.user.last_name} de {request.user.company.Company}, este es el archivo {file_path}"""
            sender_email = 'agustin@cactusco.cl'
            cc_emails = ['agustin@cactusco.cl', 'vicente@cactusco.cl']

            message1 = (
                'Recomendación de productos',
                email_cliente,  
                sender_email, 
                cc_emails
            )
            message2 = (
                f'Nueva data!! Cliente: {request.user.first_name} {request.user.last_name}, {request.user.company}',
                email_interno, 
                sender_email, 
                cc_emails
            )

            send_mass_mail((message1, message2), fail_silently=False)
            request.session['file_path'] = file_path
            request.session['available_fields'] = get_available_fields(file_path)

            return redirect(reverse('field-selection'))

        return render(request, 'welcome.html', { 'form':form })

#, { "has_submitted": True, "file_path": request.session['file_path'], "url": gc_url }
class FieldSelection(LoginRequiredMixin, View):
    available_fields = [
        ('Fecha', 'Date'), 
        ('Número de boleta', 'Bill Number'),
        ('ID de Usuario', 'User ID'),
        ('Código de producto (SKU)', 'SKU'),
        ('Cantidad de productos', 'Quant'), 
        ('Descripción del producto', 'Description')
    ]

    def get(self, request):
        form = FieldSelectionForm(available_fields=self.available_fields)
        return render(request, 'forms/field_selection.html', { 'form':form })

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
            return redirect(reverse('user-welcome'), { 'has_submitted': True,  'no_user': True })
            #render(request, 'sections/welcome.html', { 'has_submitted': True,  'no_user': True })
        
        return render(request, 'forms/field_selection.html', { 'form':form })
        
