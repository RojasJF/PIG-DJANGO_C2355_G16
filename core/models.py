from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.

class Persona2(User):
    class Meta:
        proxy = True
class Persona(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=150, verbose_name='Apellido')
    edad = models.IntegerField(verbose_name='Edad')
    mail = models.EmailField(max_length=150, verbose_name='Mail')
    dni = models.IntegerField(verbose_name='DNI', unique=True)
    
    

    class Meta:
        abstract = True
    

class Medico (Persona):
    especialidad = models.OneToOneField(
        'Especialidad',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    valor = models.IntegerField(verbose_name='Valor consulta')

    def __str__(self):
        return self.nombre
    

class Turno(models.Model):
    especialidad = models.ForeignKey(
        Especialidad,
        on_delete=models.CASCADE,
        related_name='turnos'
    )
    dni_paciente = models.IntegerField(null=True, blank=True)
    fecha_hora = models.DateTimeField(null=True)

class Paciente (Persona):
    turnos = models.ManyToManyField(
        'Turno',
        related_name='pacientes',
        blank=True
    )
    
    def solicitar_turno(self, turno):
        self.turnos.add(turno)

    def cancelar_turno(self, turno):
        self.turnos.remove(turno)

    def ver_turnos(self):
        return self.turnos.all()
    
    def __str__(self):
        return self.nombre
    
class HorarioEspecialidad(models.Model):
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    intervalo = models.IntegerField(help_text='Intervalo en minutos entre turnos')

    def generar_turnos(self):
        hora_actual = self.hora_inicio
        while hora_actual <= self.hora_fin:
            Turno.objects.create(especialidad=self.especialidad, fecha_hora=datetime.combine(self.fecha, hora_actual))
            hora_actual += timedelta(minutes=self.intervalo)


