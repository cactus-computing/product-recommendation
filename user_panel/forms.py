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
    ('Fecha', 'Fecha'),
    ('Cod', 'Codigo del Producto'),
    ('Cant', 'Cantidad Vendida')
]

class FileSubmissionForm(forms.Form):
    '''
    This is the main form in the website. It allowes a user tu submit his details and a file.
    '''
    validate_extension = FileExtensionValidator(ALLOWED_EXTENSIONS, message=f"Extension no permitida. Por favor usar un archivo alguna de las siguientes extensiones: {', '.join(ALLOWED_EXTENSIONS)}")
    document = forms.FileField(label='Excel/CSV', required=False, validators=[validate_extension])
    document.widget.attrs.update({'class' : 'form-control-file'})
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
    product_code = forms.ChoiceField(
        choices=FIELDS_2,
    )
    quantity = forms.ChoiceField(
        choices=FIELDS_2,
    )

    date.widget.attrs.update({'class' : 'form-control'})
    product_code.widget.attrs.update({'class' : 'form-control'})
    quantity.widget.attrs.update({'class' : 'form-control'})

        

    def __init__(self, available_fields=None, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['date'].label = 'Fecha'
        self.fields['product_code'].label = 'Código de producto'
        self.fields['quantity'].label = 'Cantidad'

        if available_fields is not None:
            for key in self.fields:
                self.fields[key].choices = available_fields
        