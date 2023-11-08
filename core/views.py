from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from datetime import datetime
from .forms import ContactoForm , RegisterForm, AltaEspecialidadForm
from .models import Persona, Paciente , Medico, Especialidad





def index(request):
    
    return render(request,'core/index.html')


def register(request):

    if request.method == "POST":
        formulario = RegisterForm(request.POST)

        if formulario.is_valid():
            
            messages.info(request,"Registro Exitoso")
            
            p1 = Paciente(
                nombre = formulario.cleaned_data['nombre'],
                apellido = formulario.cleaned_data['apellido'],
                dni = formulario.cleaned_data['dni'],
                edad = formulario.cleaned_data['edad'],
                mail = formulario.cleaned_data['mail'] ,
                contraseña = formulario.cleaned_data['contraseña']
            )
            p1.save()
            
            
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

class EspecialidadCreateView(CreateView):
    model = Especialidad
    template_name='core/especialidades_alta.html'
    success_url = reverse_lazy('especialidades_listado')
    fields = '__all__'
  
 


class EspecialidadDeleteView():
    pass    


class EspecialidadListView(ListView):
    model = Especialidad
    context_object_name = 'listado_especialidades'
    template_name = 'core/especialidades_listado.html'
    ordering = ['nombre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cant_registrados'] = Especialidad.objects.count()
        return context
