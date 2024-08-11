from django.urls import path
from django.contrib.auth import views as auth_views
# from . import views
from .views import  *
app_name = 'accounts'

urlpatterns =[
    path('', dashboard, name='dashboard'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),

    path('update_profile/', update_profile, name='update_profile'),
    path('update_password/', update_password, name='update_password'),


    path('forgot_password/', forgot_password, name='forgot_password'),
    path('password_reset/<uidb64>/<token>/', reset_password_confirm, name='password_reset_confirm'),


  
]