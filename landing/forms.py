from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, ButtonHolder
from django import forms
from django.forms import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator
import logging

logger = logging.Logger(__name__)

class ContactForm(forms.Form):
    '''
    This form allows the user to submit his email.
    '''
    name = forms.CharField(label='Name', max_length=250, required=True)
    email = forms.EmailField(label='Email', max_length=250, required=True)
    phone = forms.CharField(label='Name', max_length=9, min_length=9, required=False)
    message = forms.CharField(widget=forms.Textarea, max_length=1000, required=True)
    
    
    name.widget.attrs.update({'class' : 'form-control', 'placeholder': 'Nombre'})
    phone.widget.attrs.update({'class' : 'form-control', 'placeholder': 'Teléfono (opcional)'})
    message.widget.attrs.update({'class' : 'form-control', 'placeholder': 'Escribe tu mensaje'})
    email.widget.attrs.update({'class' : 'form-control', 'placeholder': 'Email'})

class SuscriptionForm(forms.Form):
    '''
    This form allows the user to submit his email.
    '''
    #name = forms.CharField(label='Name', max_length=250, required=True)
    email = forms.EmailField(label='Email', max_length=250, required=True)
    #company = forms.CharField(label='Name', max_length=250, required=True)

    #name.widget.attrs.update({'class' : 'form-control', 'placeholder': 'Nombre'})
    email.widget.attrs.update({'class' : 'form-control', 'placeholder': 'Ingresa tu email', 'type':"email", "name":"email"  })
    #company.widget.attrs.update({'class' : 'form-control', 'placeholder': 'Escribe tu mensaje'})
