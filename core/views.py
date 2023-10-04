from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime
from .forms import ContactoForm , RegisterForm
from .models import Persona


def index(request):
    
    return render(request,'core/index.html')

def register(request):

    if request.method == "POST":
        formulario = RegisterForm(request.POST)

        if formulario.is_valid():
            messages.info(request,"Registro Exitoso")
            return redirect(reverse("login"))
    else:
        formulario = RegisterForm()

    context={
        'Registro_form':formulario
    }

    return render(request, 'core/register.html',context)

def login(request):

    return render(request,'core/login.html')

def user_profile(request, user_name):

    context = {
        'user_name': user_name
    }

    return render(request, 'core/user_profile.html',context)


def solicitar_turno(request, user_name):
    context = {
        'user_name': user_name
    }

    return render(request, 'core/solicitar_turno.html',context)

def turnos_previos(request, user_name):
    context = {
        'user_name': user_name
    }

    return render(request, 'core/turnos_previos.html',context)

def mis_turnos(request, user_name):
    context = {
        'user_name': user_name
    }

    return render(request, 'core/mis_turnos.html',context)

def estudios_lab(request, user_name):
    context = {
        'user_name': user_name
    }

    return render(request, 'core/estudios_lab.html',context)

def estudios_img(request, user_name):
    context = {
        'user_name': user_name
    }


    return render(request, 'core/estudios_img.html',context)

def contact(request):
    
    if request.method == "POST":
        formulario = ContactoForm(request.POST)

        if formulario.is_valid():
          
            return redirect(reverse("login"))
    else:
        formulario = ContactoForm()

    context={
        'contacto_form':formulario
    }

    return render (request, "core/contact.html", context)