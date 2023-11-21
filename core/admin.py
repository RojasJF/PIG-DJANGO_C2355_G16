from typing import Any
from django.contrib import admin
from django.db.models.fields.related import ManyToManyField
from django.forms.models import ModelMultipleChoiceField
from django.http.request import HttpRequest
from core.models import Paciente , Medico, Turno, Especialidad

# Register your models here.

admin.site.register(Paciente)
admin.site.register(Medico)
admin.site.register(Turno)
admin.site.register(Especialidad)