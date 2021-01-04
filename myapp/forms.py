from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit 
from django import forms
from .models import Snippet
from django.core.validators import RegexValidator

class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ('name', 'last_name', 'email', 'company', 'document')
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'name',
            'last_name',
            'email',
            'company',
            'document',
            Submit('submit', 'Submit', css_class='btn-success')
        )