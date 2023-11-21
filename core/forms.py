from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Usuario, Paciente , Turno,Especialidad,Medico
from django.core.exceptions import ValidationError
from datetime import datetime, time, timedelta, date


class RegistroForm(UserCreationForm):
    dni = forms.CharField(max_length=8)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if User.objects.filter(username=dni).exists():
            raise forms.ValidationError('Este DNI ya está en uso.')
        return dni

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['dni']
        if commit:
            user.save()
            paciente = Paciente(user=user, dni=self.cleaned_data['dni'])
            paciente.save()
        return user


# class TurnoForm(forms.ModelForm):
#     horario = forms.ChoiceField(choices=[(time(hour=h // 2, minute=30 * (h % 2)).strftime('%H:%M'), time(hour=h // 2, minute=30 * (h % 2)).strftime('%H:%M')) for h in range(16, 40)])

#     class Meta:
#         model = Turno
#         fields = ['fecha', 'horario', 'paciente']

# class PacienteForm(forms.ModelForm):
#     class Meta:
#         model = Paciente
#         fields = ['user', 'dni']

# class MedicoForm(forms.ModelForm):
#     class Meta:
#         model = Medico
#         fields = ['user', 'dni']

class EspecialidadForm(forms.Form):
    especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all().order_by('nombre'))

class ContactoForm(forms.Form):
    nombre = forms.CharField(label="Nombre de contacto", required=True)
    apellido =forms.CharField(label="Apellido de contacto", widget=forms.TextInput(attrs={'class': 'fondo_rojo'}), required=True)
    edad = forms.IntegerField(label="Edad")
    mail = forms.EmailField(label="Mail", required=True)
    mensaje =  forms.CharField(widget=forms.Textarea)

    def clean_edad(self):
        if self.cleaned_data["edad"] < 18:
            raise ValidationError("El usuario no puede tener menos de 18 años")
        
        return self.cleaned_data["edad"]

    def clean(self):
        # Este if simula una busqueda en la base de datos
        # if self.cleaned_data["nombre"] == "Carlos" and self.cleaned_data["apellido"] == "Lopez":
            #raise ValidationError("El usuario Carlos Lopez ya existe")
        
        # Si el usuario no existe lo damos de alta

        return self.cleaned_data
    
    

class AltaEspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = '__all__'



class RegistroMedicoForm(UserCreationForm):
    dni = forms.CharField(max_length=8)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if User.objects.filter(username=dni).exists():
            raise forms.ValidationError('Este DNI ya está en uso.')
        return dni

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['dni']
        if commit:
            user.save()
            medico = Medico(user=user, dni=self.cleaned_data['dni'])
            medico.save()
        return user

class TurnoSinPacienteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TurnoSinPacienteForm, self).__init__(*args, **kwargs)
        HORARIO_INICIO = datetime.combine(date.today(), time(hour=9))  # 9:00 AM
        HORARIO_FIN = HORARIO_INICIO + timedelta(hours=8)  # 8 horas después del inicio
        INTERVALO = timedelta(minutes=30)

        horarios = [(t.time().strftime('%H:%M'), t.time().strftime('%H:%M')) for t in
                    [HORARIO_INICIO + i * INTERVALO for i in
                     range(((HORARIO_FIN - HORARIO_INICIO).seconds // INTERVALO.seconds) + 1)]]

        self.fields['horario'] = forms.ChoiceField(choices=horarios)

    class Meta:
        model = Turno
        exclude = ['paciente']
class SeleccionarEspecialidadForm(forms.Form):
    especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all())

class SeleccionarTurnoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        turnos_disponibles = kwargs.pop('turnos_disponibles')
        super().__init__(*args, **kwargs)
        self.fields['turno'] = forms.ModelChoiceField(queryset=turnos_disponibles)


class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['fecha', 'horario', 'especialidad']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'especialidad': forms.Select(attrs={'id': 'id_especialidad'}),
            'turno': forms.Select(attrs={'id': 'id_turno'}),
        }

class TurnoCancelForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = []

class SolicitarTurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['especialidad']

class AsignarTurnoForm(forms.Form):
    turno = forms.ModelChoiceField(queryset=Turno.objects.none())