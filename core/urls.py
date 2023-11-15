from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

# from core.admin import sitio_admin

urlpatterns = [

    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html'),name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path ('',views.index, name='index'),
    path ('register',views.register, name='register'),
    path ('login',views.login, name='login'),
    path ('profile/<int:dni>',views.user_profile, name='profile'),
    path ('turnos_previos/<int:dni>' ,views.turnos_previos, name='turnos_previos'),
    path ('mis_turnos/<int:dni>' ,views.mis_turnos, name='mis_turnos'),
    path ('estudios_lab/<int:dni>' ,views.estudios_lab, name='estudios_lab'),
    path ('estudios_img/<int:dni>' ,views.estudios_img, name='estudios_img'),
    path ('contact' ,views.contact, name='contact'),
    path ('especialidades/alta' ,views.EspecialidadCreateView.as_view(), name='especialidades_alta'),
    path ('especialidades/listado' ,views.EspecialidadListView.as_view(), name='especialidades_listado'),
    path('solicitar_turno/<int:dni>/', views.solicitar_turno, name='solicitar_turno'),
    path('cancelar_turno/<int:dni>/<int:turno_id>/', views.cancelar_turno, name='cancelar_turno'),
    path('mis_turnos/<int:dni>/', views.mis_turnos, name='ver_turnos'),
    path('cargar_fechas_turnos/<int:id_especialidad>/', views.cargar_fechas_turnos, name='cargar_fechas_turnos'),

]