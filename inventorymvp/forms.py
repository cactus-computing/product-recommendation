from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, ButtonHolder
from django import forms
from django.forms import ValidationError
#from .models import User, CompanyData
from django.core.validators import RegexValidator, FileExtensionValidator
import logging

logger = logging.Logger(__name__)

ALLOWED_EXTENSIONS = [
    'csv',
    'xlsx',
    'xls'
]



class FileSubmissionForm(forms.Form):
    validate_extension = FileExtensionValidator(ALLOWED_EXTENSIONS, message=f"Extension no permitida. Por favor usar un archivo alguna de las siguientes extensiones: {', '.join(ALLOWED_EXTENSIONS)}")


    name = forms.CharField(label='Nombre', max_length=180, required=True)
    last_name = forms.CharField(label='Apellido', max_length=180, required=True)
    email = forms.EmailField(label='Email', max_length=180, required=True)
    company = forms.CharField(label='Empresa', max_length=180, required=True)

    document = forms.FileField(label='Excel/CSV', required=False, validators=[validate_extension])
    recieve_info_flag = forms.BooleanField(label='Suscribirme a la lista de mails', required=False)
    
    name.widget.attrs.update({'class' : 'form-control'})
    last_name.widget.attrs.update({'class' : 'form-control'})
    email.widget.attrs.update({'class' : 'form-control'})
    company.widget.attrs.update({'class' : 'form-control'})
    document.widget.attrs.update({'class' : 'form-control-file'})
    recieve_info_flag.widget.attrs.update({'class' : 'form-check'})

    def clean_extensions(self):
        ext = self.cleaned_data['document'].name.split('.')[-1]
        logger.info(ext)
        logger.info('validation cycle')
        if ext not in ALLOWED_EXTENSIONS:
            raise ValidationError(('Extension no permitida'), code='invalid')
        
        return self.cleaned_data