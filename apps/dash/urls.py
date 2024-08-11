from django.urls import path
from django.contrib.auth import views as auth_views
from .views import  *
app_name = 'dashboard'

urlpatterns =[
    path('', my_view, name='my_view'),
   
]