from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    
    return render(request,'core/index.html')

def register(request):

    return render(request, 'core/register.html')

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

def contact(request,user_name):

    context = {
        'user_name': user_name
    }
    
    return render(request,'core/contact.html',context)

