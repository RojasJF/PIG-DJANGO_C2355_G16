from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views
from .views import TurnoListView, PacienteTurnosListView

# from core.admin import sitio_admin

urlpatterns = [

    path ('login/', auth_views.LoginView.as_view(template_name='core/login.html'),name='login'),
    path ('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path ('',views.index, name='index'),
    path ('register',views.register, name='register'),
    path ('profile/', views.user_profile, name='profile'),
    path('mis_turnos/', PacienteTurnosListView.as_view(), name='mis_turnos'),
    path ('solicitar_turno/', views.solicitar_turno, name='solicitar_turno'),
    path('cancelar_turno/<int:turno_id>/', views.cancelar_turno, name='cancelar_turno'),
    path('contact/<str:username>/', views.contact, name='contact'),
    path ('especialidades/alta' ,views.EspecialidadCreateView.as_view(), name='especialidades_alta'),
    path ('turnos/', TurnoListView.as_view(), name='turnos'),
    path ('medico/alta' ,views.register_medico, name='register_medico'),
    path ('crear_turno/', views.crear_turno, name='crear_turno'),
    path ('turnos_disponibles/', views.turnos_disponibles, name='turnos_disponibles'),
    # # path('cargar_fechas_turnos/<int:id_especialidad>/', views.cargar_fechas_turnos, name='cargar_fechas_turnos'),


]