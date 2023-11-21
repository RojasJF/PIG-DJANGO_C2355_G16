from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from datetime import datetime, date, time, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from .models import User,Paciente,Turno,Especialidad
from .forms import RegistroForm,TurnoForm,ContactoForm,AltaEspecialidadForm,RegistroMedicoForm,SeleccionarTurnoForm,SeleccionarEspecialidadForm,TurnoCancelForm,EspecialidadForm,AsignarTurnoForm
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
def solicitar_turno(request):
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            especialidad = form.cleaned_data.get('especialidad')
            request.session['especialidad_id'] = especialidad.id
            return redirect('turnos_disponibles')
    else:
        form = EspecialidadForm()
    return render(request, 'core/solicitar_turno.html', {'form': form})

@login_required
def turnos_disponibles(request):
    especialidad_id = request.session.get('especialidad_id')
    if especialidad_id is not None:
        turnos = Turno.objects.filter(especialidad_id=especialidad_id)
        if request.method == 'POST':
            form = AsignarTurnoForm(request.POST)
            form.fields['turno'].queryset = turnos
            if form.is_valid():
                turno = form.cleaned_data.get('turno')
                # Aquí puedes asignar el turno al paciente
                paciente = Paciente.objects.get(user=request.user)
                paciente.turnos.add(turno)
                return redirect('mis_turnos')
        else:
            form = AsignarTurnoForm()
            form.fields['turno'].queryset = turnos
    else:
        form = AsignarTurnoForm()
        turnos = Turno.objects.none()
    return render(request, 'core/turnos_disponibles.html', {'form': form, 'turnos': turnos})


class PacienteTurnosListView(ListView):
    model = Paciente
    context_object_name = 'paciente_turnos'
    template_name = 'core/paciente_turnos.html'

    def get_queryset(self):
        return Paciente.objects.filter(user=self.request.user)

@login_required
def cancelar_turno(request, turno_id):
    if request.method == 'POST':
        turno = get_object_or_404(Turno, id=turno_id)
        turno.delete()
    return redirect('mis_turnos')


def contact(request, username):
    if request.method == "POST":
        formulario = ContactoForm(request.POST)

        if formulario.is_valid():
            return redirect(reverse("login"))
    else:
        formulario = ContactoForm()

    context={
        'contacto_form':formulario,
        'username': username
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


class TurnoListView(ListView):
    model = Turno
    context_object_name = 'turnos'
    template_name = 'core/turnos_listado.html'

    def get_queryset(self):
        return Turno.objects.select_related('especialidad', 'especialidad__medico').order_by('especialidad__nombre', 'especialidad__medico__user__username', 'fecha', 'horario')
    

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
        form = TurnoForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data.get('fecha')
            especialidad = form.cleaned_data.get('especialidad')
            inicio = time(hour=8)
            fin = time(hour=16)
            while inicio <= fin:
                Turno.objects.create(fecha=fecha, horario=inicio, especialidad=especialidad)
                inicio = (datetime.combine(date.today(), inicio) + timedelta(minutes=30)).time()
            return redirect('crear_turno')
    else:
        form = TurnoForm()
    return render(request, 'core/crear_turno.html', {'form': form})