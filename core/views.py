from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request,"index.html")

def register(request):
    return HttpResponse(
        f"Bienvenido al registro"

    )

def login(request):
    return HttpResponse(
        f"Bienvenido al login"

    )

def user_profile(request, user_name):
    return HttpResponse(
        f"Bienvendo {user_name}"
        
    )