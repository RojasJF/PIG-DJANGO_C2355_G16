from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from datetime import time, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from .models import User,Paciente,Turno,Especialidad
from .forms import RegistroForm,TurnoForm,ContactoForm,AltaEspecialidadForm,RegistroMedicoForm,TurnoSinPacienteForm,EspecialidadForm,SeleccionarTurnoForm,SeleccionarEspecialidadForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group

def index(request):
    
    return render(request,'core/index.html')


def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Obtén el grupo
            group = Group.objects.get(name='Pacientes')
            # Añade el usuario al grupo
            group.user_set.add(user)
            return redirect('login')
    else:

        form = RegistroForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def user_profile(request):
    return render(request, 'core/user_profile.html', {'user': request.user})

@login_required
def seleccionar_especialidad(request):
    if request.method == 'POST':
        form = SeleccionarEspecialidadForm(request.POST)
        if form.is_valid():
            request.session['especialidad_id'] = form.cleaned_data['especialidad'].id
            return redirect('solicitar_turno')
    else:
        form = SeleccionarEspecialidadForm()
    return render(request, 'core/seleccionar_especialidad.html', {'form': form})

@login_required
def solicitar_turno(request):
    especialidad_id = request.session.get('especialidad_id')
    if not especialidad_id:
        return redirect('seleccionar_especialidad')
    especialidad = Especialidad.objects.get(id=especialidad_id)
    turnos_disponibles = Turno.objects.filter(especialidades=especialidad, paciente=None)
    if request.method == 'POST':
        form = SeleccionarTurnoForm(request.POST, turnos_disponibles=turnos_disponibles)
        if form.is_valid():
            turno = form.cleaned_data['turno']
            turno.paciente = Paciente.objects.get(user=request.user)
            turno.save()
            return redirect('ver_turnos', username=request.user.username)
    else:
        form = SeleccionarTurnoForm(turnos_disponibles=turnos_disponibles)
    return render(request, 'core/solicitar_turno.html', {'form': form})



@login_required
def seleccionar_turno(request):
    if request.method == 'POST':
        form = SeleccionarTurnoForm(request.POST, turnos_disponibles=request.session['turnos_disponibles'])
        if form.is_valid():
            turno = form.cleaned_data['turno']
            turno.paciente = Paciente.objects.get(user=request.user)
            turno.save()
            return redirect('ver_turnos')
    else:
        form = SeleccionarTurnoForm(turnos_disponibles=request.session['turnos_disponibles'])
    return render(request, 'core/seleccionar_turno.html', {'form': form})


@login_required
def ver_turnos(request, username):
    user = User.objects.get(username=username)
    paciente = Paciente.objects.get(user=user)
    turnos = Turno.objects.filter(paciente=paciente)
    return render(request, 'core/ver_turnos.html', {'turnos': turnos})

@login_required
def cancelar_turno(request, turno_id):
    turno = Turno.objects.get(id=turno_id)
    if request.method == 'POST':
        turno.delete()
        return redirect('ver_turnos')
    return render(request, 'core/cancelar_turno_confirm.html', {'turno': turno})


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


def register_medico(request):
    if request.method == 'POST':
        form = RegistroMedicoForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Obtén el grupo
            group = Group.objects.get(name='Staff')
            # Añade el usuario al grupo
            group.user_set.add(user)
            return redirect('login')
    else:
        form = RegistroMedicoForm()
    return render(request, 'core/register_medico.html', {'form': form})

class EspecialidadCreateView(PermissionRequiredMixin,CreateView):
    permission_required = 'core.add_especialidad'

    model = Especialidad
    template_name='core/especialidades_alta.html'
    success_url = reverse_lazy('especialidades_listado')
    fields = '__all__'
  
 



class EspecialidadDeleteView(LoginRequiredMixin):
    pass    


class EspecialidadListView(LoginRequiredMixin, ListView):

    model = Especialidad
    context_object_name = 'listado_especialidades'
    template_name = 'core/especialidades_listado.html'
    ordering = ['nombre']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cant_registrados'] = Especialidad.objects.count()
        context['especialidades'] = Especialidad.objects.prefetch_related('turnos')  # Agrega las especialidades con sus turnos al contexto
        return context
    

@permission_required('core.add_especialidad')
def alta_especialidad(request):
    if request.method == 'POST':
        form = AltaEspecialidadForm(request.POST)
        if form.is_valid():
            form.save()
            # Aquí puedes redirigir a donde quieras después de guardar el formulario
    else:
        form = AltaEspecialidadForm()

    

    return render(request, 'especilidades_alta.html', {'form': form})




@permission_required('core.add_turno')
def crear_turno(request):
    if request.method == 'POST':
        form = TurnoSinPacienteForm(request.POST)
        if form.is_valid():
            turno = form.save()
            return redirect('crear_turno')
    else:
        form = TurnoSinPacienteForm()
    return render(request, 'core/crear_turno.html', {'form': form})

