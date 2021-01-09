from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import utils
from .forms import FileSubmissionForm
from .models import User, CompanyData, handle_uploaded_file
#from .storage import upload_blob
import logging
from django.core.mail import send_mail

logger = logging.Logger(__name__)


def snippet_detail(request):
    if request.method == "POST":
        form = FileSubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            company = form.cleaned_data['company']
            recieve_info_flag = form.cleaned_data['recieve_info_flag']
            user = User(name=name, last_name=last_name, email=email, company=company, recieve_info_flag=recieve_info_flag)

            try:
                user.save()
            except utils.IntegrityError:
                user = User.objects.get(email=email)
            
            file_path_or_url = handle_uploaded_file(request.FILES['document'], company=company)
            stored_file = CompanyData(document_location=file_path_or_url, user=user)
            stored_file.save()
            email_message = f"""Hola, {name}!\n\nTu data está siendo procesada y te enviarémos un correo a penas tengamos el resultado.\n\nGracias por confiar en nosotros!\n\nEquipo de StockApp"""
            
            send_mail(
                subject='StockApp Forecasting',
                message=email_message,
                from_email='agustin.escobar@cactusco.cl',
                recipient_list=[email],
                fail_silently=False,
            )
            return render(request, 'form/form.html', { 'user': user, 'has_submitted': True })
    else:
        form = FileSubmissionForm

    return render(request, 'form/form.html', { 'form':form, 'has_submitted': False })

