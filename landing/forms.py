from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, ButtonHolder
from django import forms
from django.forms import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator
import logging

logger = logging.Logger(__name__)

class UserRegistration(forms.Form):
    '''
    This is the main form in the website. It allowes a user tu submit his details and a file.
    '''
    
    email = forms.EmailField(label='Email', max_length=250, required=True)
    email.widget.attrs.update({'class' : 'form-control', 'placeholder': 'Email'})
