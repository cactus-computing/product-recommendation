from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, ButtonHolder
from django import forms
#from .models import User, CompanyData
from django.core.validators import RegexValidator

class FileSubmissionForm(forms.Form):
    name = forms.CharField(label='Nombre', max_length=180)
    last_name = forms.CharField(label='Apellido', max_length=180)
    email = forms.EmailField(label='Email', max_length=180)
    company = forms.CharField(label='Empresa', max_length=180)
    
    document = forms.FileField(label='Excel/CSV', required=False)
    recieve_info_flag = forms.BooleanField(label='Suscribirme a la lista de mails', required=False)
    
    name.widget.attrs.update({'class' : 'form-control'})
    last_name.widget.attrs.update({'class' : 'form-control'})
    email.widget.attrs.update({'class' : 'form-control'})
    company.widget.attrs.update({'class' : 'form-control'})
    document.widget.attrs.update({'class' : 'form-control-file'})
    recieve_info_flag.widget.attrs.update({'class' : 'form-check'})