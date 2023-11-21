from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=8, unique=True)

    def save(self, *args, **kwargs):
        self.user.username = self.dni
        self.user.save()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Medico(Usuario):

    def __str__(self):
        return self.user.username

class Paciente(Usuario):
    def __str__(self):
        return self.user.username

class Turno(models.Model):
    fecha = models.DateField()
    horario = models.TimeField()
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f'{self.fecha} {self.horario}  - {self.paciente}'

class Especialidad(models.Model):
    nombre = models.CharField(max_length=200)
    turnos = models.ManyToManyField('Turno', related_name='especialidades')
    medico = models.ForeignKey('Medico', on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
