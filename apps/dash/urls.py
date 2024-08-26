from django.urls import path
from django.contrib.auth import views as auth_views
from .views import  *
app_name = 'dashboard'

urlpatterns =[
    path('', my_ip, name='my_view'),
    path('registro de asistencia/', register_assistant, name='register_assistant'),
    path('listar usuarios/', listUser, name='list_users'),
    path('listar grupos/', listGroups, name='listGroups'),

    path('asignar actividades/', assignActivity, name='assignActivity'),
    path('listar actividades/', listActivitys, name='listActivitys'),
    path('actividad/<int:id>', list_activity, name='id_activity'),
    path('elimnar actividad/<int:id>', clear_activity, name='clear_activity'),
    path('editar actividad/<int:id>', edit_activity, name='edit_activity'),

    path('get_users_by_group/', get_users_by_group, name='get_users_by_group'),
   
]