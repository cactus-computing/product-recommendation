from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
#from django.utils.http import urlencode
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

class ProtectView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'welcome.html')

def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()
        
            # Si el usuario se crea correctamente 
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "register.html", {'form': form})

