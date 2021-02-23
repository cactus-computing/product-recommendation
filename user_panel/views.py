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

from .models import User, Company
from .storage import rename_dataset

class Welcome(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'welcome.html')

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
        '''
        Field selection page handling.
        '''

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
            return render(request, 'sections/welcome.html', { 'has_submitted': True,  'no_user': True })