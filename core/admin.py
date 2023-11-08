from django.contrib import admin
from core.models import Paciente , Medico, Turno, Especialidad

# Register your models here.
admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Turno)
admin.site.register(Especialidad)