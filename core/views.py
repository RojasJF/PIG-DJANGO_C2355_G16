from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from datetime import datetime
from .forms import ContactoForm , RegisterForm, AltaEspecialidadForm, TurnoForm , FechaTurnoForm
from .models import Persona, Paciente , Medico, Especialidad, Turno
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required



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
    if request.method == 'POST':
        dni = request.POST['dni']
        try:
            paciente = Paciente.objects.get(dni=dni)
            return redirect('/Clinica/profile/' + dni)
        except Paciente.DoesNotExist:
            messages.error(request, 'DNI no encontrado')
            return redirect('login')
    else:
        return render(request, 'core/login.html')


def user_profile(request, dni):
    paciente = Paciente.objects.get(dni=dni)
    context = {
        'nombre': paciente.nombre,
        'apellido': paciente.apellido,
        'edad': paciente.edad,
        'mail': paciente.mail,
        'dni': paciente.dni,
    }

    return render(request, 'core/user_profile.html',context)




def solicitar_turno(request, dni):
    paciente = get_object_or_404(Paciente, dni=dni)
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            turno = form.save(commit=False)
            turno.paciente = paciente
            turno.dni_paciente = paciente.dni  # Guardamos el DNI del paciente en el turno
            turno.save()
            messages.success(request, 'Turno solicitado con éxito')
            return redirect('mis_turnos', dni=dni)
    else:
        form = TurnoForm()
    return render(request, 'core/solicitar_turno.html', {'form': form, 'dni': dni})

def mis_turnos(request, dni):
    # Obtenemos los turnos donde el DNI del paciente coincide con el DNI proporcionado
    turnos = Turno.objects.filter(dni_paciente=dni)
    return render(request, 'core/mis_turnos.html', {'turnos': turnos, 'dni': dni})



def cancelar_turno(request, dni, turno_id):
    paciente = get_object_or_404(Paciente, dni=dni)
    # Buscamos el turno usando el ID del turno y el DNI del paciente
    turno = get_object_or_404(Turno, id=turno_id, dni_paciente=dni)
    if Turno.objects.filter(id=turno_id).exists():  # Verificamos si el turno existe en la tabla de turnos
        paciente.turnos.remove(turno)  # Eliminamos el turno de los turnos del paciente
        turno.delete()  # Eliminamos el turno de la base de datos          
        messages.success(request, 'Turno cancelado con éxito')
    else:
        messages.error(request, 'El turno no existe')
    return redirect('mis_turnos', dni=dni)



def turnos_previos(request, user_name): 
    context = {
        'user_name': user_name
    }

    return render(request, 'core/turnos_previos.html',context)


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


class EspecialidadCreateView(PermissionRequiredMixin,CreateView):
    permission_required = 'core.add_especialidad'
    model = Especialidad
    template_name='core/especialidades_alta.html'
    success_url = reverse_lazy('especialidades_listado')
    fields = '__all__'
  
 


class EspecialidadDeleteView(LoginRequiredMixin):
    pass    


class EspecialidadListView(LoginRequiredMixin,ListView):
    model = Especialidad
    context_object_name = 'listado_especialidades'
    template_name = 'core/especialidades_listado.html'
    ordering = ['nombre']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cant_registrados'] = Especialidad.objects.count()
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

@login_required
def cargar_fechas_turnos(request, id_especialidad):
    especialidad = Especialidad.objects.get(id=id_especialidad)
    if request.method == 'POST':
        form = FechaTurnoForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_fin = form.cleaned_data['hora_fin']
            intervalo = form.cleaned_data['intervalo']
            hora_actual = hora_inicio
            while hora_actual <= hora_fin:
                fecha_hora = datetime.combine(fecha, hora_actual)
                Turno.objects.create(especialidad=especialidad, fecha_hora=fecha_hora)
                hora_actual = (datetime.combine(fecha, hora_actual) + timedelta(minutes=intervalo)).time()
            return redirect('index')
    else:
        form = FechaTurnoForm()
    return render(request, 'cargar_fechas_turnos.html', {'form': form})