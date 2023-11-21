from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

# from core.admin import sitio_admin

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path ('',views.index, name='index'),
    path ('register',views.register, name='register'),
    path('profile/', views.user_profile, name='profile'),
    path ('ver_turnos/<str:username>/' ,views.ver_turnos, name='ver_turnos'),
    path('solicitar_turno/', views.solicitar_turno, name='solicitar_turno'),
    path('cancelar_turno/<int:turno_id>/', views.cancelar_turno, name='cancelar_turno'),
    path ('estudios_lab' ,views.estudios_lab, name='estudios_lab'),
    path ('estudios_img' ,views.estudios_img, name='estudios_img'),
    path ('contact' ,views.contact, name='contact'),
    path ('especialidades/alta' ,views.EspecialidadCreateView.as_view(), name='especialidades_alta'),
    path ('especialidades/listado' ,views.EspecialidadListView.as_view(), name='especialidades_listado'),
    path ('medico/alta' ,views.register_medico, name='register_medico'),
    path('crear_turno/', views.crear_turno, name='crear_turno'),
    path('seleccionar_turno/', views.seleccionar_turno, name='seleccionar_turno'),
    path('seleccionar_especialidad/', views.seleccionar_especialidad, name='seleccionar_especialidad'),

    # # path('cargar_fechas_turnos/<int:id_especialidad>/', views.cargar_fechas_turnos, name='cargar_fechas_turnos'),

]