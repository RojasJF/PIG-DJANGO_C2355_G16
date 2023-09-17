from django.urls import path
from . import views

urlpatterns = [
    path ('',views.index, name='index'),
    path ('register',views.register, name='register'),
    path ('login',views.login, name='login'),
    path ('profile/<str:user_name>',views.user_profile, name='profile'),
    path ('solicitar_turno/<str:user_name>' ,views.solicitar_turno, name='solicitar_turno'),
    path ('turnos_previos/<str:user_name>' ,views.turnos_previos, name='turnos_previos'),
    path ('mis_turnos/<str:user_name>' ,views.mis_turnos, name='mis_turnos'),
    path ('estudios_lab/<str:user_name>' ,views.estudios_lab, name='estudios_lab'),
    path ('estudios_img/<str:user_name>' ,views.estudios_img, name='estudios_img'),
    path ('contact/<str:user_name>' ,views.contact, name='contact'),
]