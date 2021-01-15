from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, ButtonHolder
from django import forms
from django.forms import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator
import logging

logger = logging.Logger(__name__)

class UserRegistration(forms.Form):
    '''
    This form allows the user to submit his email.
    '''
    
    email = forms.EmailField(label='Email', max_length=250, required=True)
    email.widget.attrs.update({'class' : 'form-control', 'placeholder': 'Email'})
