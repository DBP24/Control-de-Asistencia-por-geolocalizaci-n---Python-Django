from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def my_view(request):
    user_ip = request.META.get('REMOTE_ADDR')
    return HttpResponse(f'Your IP address is {user_ip}')

"""
https://ip.guide/
https://ip.guide/190.236.8.116
busqueda de informacion de ip , hacer ubicacion de visitante y mostrar informacion de acuerdo al lugar
"""
