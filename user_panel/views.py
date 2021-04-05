from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as do_logout
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FieldSelectionForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .forms import FileSubmissionForm, FieldSelectionForm
from .models import User, Company, CompanyData
import logging
from django.core.mail import send_mail, send_mass_mail
from django.template import Context, loader

