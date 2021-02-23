from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

class ProtectView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'welcome.html')


