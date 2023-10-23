from django.db import models

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido = models.CharField(max_length=150, verbose_name='Apellido')
    edad = models.IntegerField(verbose_name='Edad')
    mail = models.EmailField(max_length=150, verbose_name='Mail')
    contraseña = models.CharField(max_length=150, verbose_name='Contraseña')
    dni = models.IntegerField(verbose_name='DNI')
    turnos = models.CharField(max_length=50, verbose_name='Turnos')

    class Meta:
        abstract = True

class Paciente (Persona):
    legajo = models.CharField(max_length=100, verbose_name='Legajo')
    

class Medico (Persona):
    matricula = models.IntegerField(verbose_name='Matricula')

class Turno(models.Model):
    fecha = models.DateField(verbose_name='Fecha del Turno')

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.CharField(max_length=100, verbose_name='Descripcion')
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico,on_delete=models.CASCADE)
    paciente = models.ManyToManyField(Paciente)



    
