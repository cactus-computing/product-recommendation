from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, ButtonHolder
from django import forms
from django.forms import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator
import logging

logger = logging.Logger(__name__)

ALLOWED_EXTENSIONS = [
    'csv',
    'xlsx',
    'xls'
]

FIELDS = [
    'Fecha',
    'Codigo del Producto',
    'Cantidad Vendida'
]

FIELDS_2 = [
    ('Fecha', 'Date'), 
    ('Número de boleta', 'Bill Number'),
    ('ID de Usuario', 'User ID'),
    ('Código de producto (SKU)', 'SKU'),
    ('Cantidad de productos', 'Quant'), 
    ('Descripción del producto', 'Description')
]

class FileSubmissionForm(forms.Form):
    '''
    This is the main form in the website. It allowes a user tu submit his details and a file.
    '''
    validate_extension = FileExtensionValidator(ALLOWED_EXTENSIONS, message=f"Extension no permitida. Por favor usar un archivo alguna de las siguientes extensiones: {', '.join(ALLOWED_EXTENSIONS)}")

    name = forms.CharField(label='Name', max_length=250, required=True)
    last_name = forms.CharField(label='Last Name', max_length=250, required=True)
    email = forms.EmailField(label='Email', max_length=250, required=True)
    phone = forms.CharField(label='Phone', max_length=12, required=True)
    company = forms.CharField(label='Company', max_length=250, required=True)

    document = forms.FileField(label='Excel/CSV', required=False, validators=[validate_extension])
    recieve_info_flag = forms.BooleanField(label='Suscribirme a la lista de mails', required=False)
    
    name.widget.attrs.update({'class' : 'form-control', 'placeholder': 'Nombre'})
    last_name.widget.attrs.update({'class' : 'form-control', 'placeholder': 'Apellido'})
    email.widget.attrs.update({'class' : 'form-control', 'placeholder': 'Email'})
    phone.widget.attrs.update({'class' : 'form-control', 'placeholder': 'Telefono'})
    company.widget.attrs.update({'class' : 'form-control', 'placeholder': 'Empresa'})
    document.widget.attrs.update({'class' : 'form-control-file'})
    recieve_info_flag.widget.attrs.update({'class' : 'form-check'})

    def clean_extensions(self):
        ext = self.cleaned_data['document'].name.split('.')[-1]
        logger.info(ext)
        logger.info('validation cycle')
        if ext not in ALLOWED_EXTENSIONS:
            raise ValidationError(('Extension no permitida'), code='invalid')
        
        return self.cleaned_data

class FieldSelectionForm(forms.Form):
    '''
    This form allows a user to rename his/her file fields according to our standard.
    '''
    date = forms.ChoiceField(
        choices=FIELDS_2,
    )
    bill_number = forms.ChoiceField(
        choices=FIELDS_2,
    )
    user_id = forms.ChoiceField(
        choices=FIELDS_2,
    )
    product_code = forms.ChoiceField(
        choices=FIELDS_2,
    )
    quantity = forms.ChoiceField(
        choices=FIELDS_2,
    )
    description = forms.ChoiceField(
        choices=FIELDS_2,
    )

    date.widget.attrs.update({'class' : 'form-control'})
    bill_number.widget.attrs.update({'class' : 'form-control'})
    user_id.widget.attrs.update({'class' : 'form-control'})
    product_code.widget.attrs.update({'class' : 'form-control'})
    quantity.widget.attrs.update({'class' : 'form-control'})
    description.widget.attrs.update({'class' : 'form-control'})        

    def __init__(self, available_fields=None, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['date'].label = 'Fecha'
        self.fields['bill_number'].label = 'Número de boleta'
        self.fields['user_id'].label = 'ID de Usuario'
        self.fields['product_code'].label = 'Código del producto (SKU)'
        self.fields['quantity'].label = 'Cantidad de productos'
        self.fields['description'].label = 'Cantidad de productos'

        if available_fields is not None:
            for key in self.fields:
                self.fields[key].choices = available_fields
        