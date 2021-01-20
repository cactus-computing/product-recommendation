from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db import utils
from .forms import FileSubmissionForm, FieldSelectionForm
from .models import User, CompanyData, handle_uploaded_file, get_available_fields, rename_dataset
import logging
from django.core.mail import send_mail, send_mass_mail
from django.urls import reverse
from django.template import Context, loader

logger = logging.Logger(__name__)


def main_form(request):
    '''
    Main function for handling landing page operations and form submission.
    Parameters:
        - request: contains the details of the user as well as the file in the .POST and .FILES method.
    Returns:
        - conditional to program flow: renders the landing page or redirects to the field selection form (field_selection function).
    '''
    if request.method == "POST":
        form = FileSubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            company = form.cleaned_data['company']
            recieve_info_flag = form.cleaned_data['recieve_info_flag']
            user = User(name=name, last_name=last_name, email=email, company=company, recieve_info_flag=recieve_info_flag)

            try:
                user.save()
            except utils.IntegrityError:
                user = User.objects.get(email=email)
            
            file_path, gc_url = handle_uploaded_file(request.FILES['document'], company=company, local=False)
            stored_file = CompanyData(document_location=file_path, user=user)
            stored_file.save()

            email_cliente = f"""Hola, {name}!\n\nTu data está siendo procesada y te enviarémos un correo a penas tengamos el resultado.\n\nGracias por confiar en nosotros!\n\nEquipo de StockApp"""
            email_interno = f"""Datos del nuevo contacto:\n\nNombre:{name} {last_name}\n\nEmpresa: {company}\n\nEmail: {email}\n\nTelefono: {phone}\n\nEmail info: {recieve_info_flag}"""
            
            message1 = (
                'StockApp Forecasting',
                email_cliente,  
                'agustin.escobar@cactusco.cl', 
                [email]
            )

            message2 = (
                f'Nuevo Registro!! Cliente: {name} {last_name}, {company}',
                email_interno, 
                'agustin.escobar@cactusco.cl', 
                ['agustin.escobar@cactusco.cl', 'vicente.escobar@cactusco.cl', 'rodrigo.oyarzun25@gmail.com']
            )

            send_mass_mail((message1, message2), fail_silently=False)

            request.session['file_path'] = file_path
            request.session['available_fields'] = get_available_fields(file_path)
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('field-selection'))
    else:
        form = FileSubmissionForm

    return render(request, 'form/form.html', { 'form':form, 'has_submitted': False })


def field_selection(request):
    '''
    Field selection page handling.
    Parameters:
        - request: request.POST contains the form data
    Returns:
        - renders the field selection form to rename the uploaded dataframes or if handled correctly
        it redirects to the Landing Page
    '''

    if request.session['available_fields'] is None:
        available_fields = [
            ('Date', 'Date'), 
            ('Quant','Quant'), 
            ('SKU', 'SKU')
        ]
    else:
        available_fields = []
        for key in request.session['available_fields']:
            available_fields.append((key, key))


    if request.method == "POST":
        form = FieldSelectionForm(available_fields, request.POST)
        
        user = get_object_or_404(User, pk=request.session['user_id'])
        if form.is_valid():
            rename_dataset(request.session['file_path'], form.cleaned_data)
            return render(request, 'form/form.html', { 'user': user, 'has_submitted': True,  'no_user': True })
    else:
        form = FieldSelectionForm(available_fields=available_fields)

    return render(request, 'form/field_selection.html', { 'form':form })

def error404(request, exception):
    template = loader.get_template('404.html')
    context = Context({
        'message': 'All: %s' % request,
        })
    return HttpResponse(content=template.render(context), content_type='text/html; charset=utf-8', status=404)