from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db import utils
from .forms import UserRegistration
from .models import User
import logging
from django.core.mail import send_mail, send_mass_mail
from django.urls import reverse
from django.template import Context, loader

logger = logging.Logger(__name__)

def landing(request):
    '''
    Main function for handling landing page operations and form submission.
    Parameters:
        - request: contains the details of the user email in the .POST attribute.
    Returns:
        - conditional to program flow: renders the landing page or redirects to the field selection form (field_selection function).
    '''
    submitted = False
    if request.method == "POST":
        form = UserRegistration(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            new_user = User(email=email)
            try:
                new_user.save()
            except utils.IntegrityError:
                user = User.objects.get(email=email)
            
            submitted = True

    form = UserRegistration

    return render(request, 'landing.html', { 'form':form, 'has_submitted': submitted })   


def error404(request, exception):
    template = loader.get_template('404.html')
    context = Context({
        'message': 'All: %s' % request,
        })
    return HttpResponse(content=template.render(context), content_type='text/html; charset=utf-8', status=404) 