from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from cvexpert.utils import *
from django.contrib import messages
from .models import RegisterAssistant

from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def my_ip(request):
    user_ip = request.META.get('REMOTE_ADDR')
    return HttpResponse(f'Your IP address is {user_ip}')

"""
https://ip.guide/
https://ip.guide/190.236.8.116
busqueda de informacion de ip , hacer ubicacion de visitante y mostrar informacion de acuerdo al lugar
"""

@login_required()
def register_assistant(request):
    limpiar_messages(request,messages)  
    context = identify_role(request)
    # verificar si marco asistencia
    try: 
        now =  timezone.now()
        users_ = RegisterAssistant.objects.filter(date_created=now).filter(name=str(request.user))
        if users_:
            # validar si ya marco salida
            for quer in users_:
                if quer.time_out:
                    messages.success(request,"YA REGISTRO SU ASISTENCIA NO OLVIDE SUBIR SUS REPORTES")
                    return redirect('accounts:dashboard')
                else:
                    mensaje = "Registre su SALIDA y NO OLVIDE SUBIR EL REPORTE DE SUS ACTIVIDADES"
                    context.update({'income':True , 'mensaje':mensaje})

           
          
        else:
            mensaje = "Bienvenido, registre su Ingreso y NO OLVIDE SUBIR EL REPORTE DE SUS ACTIVIDADES"
            context.update({'income':False , 'mensaje':mensaje})
       
        if request.method == 'POST':
    # Ingreso
            if request.POST.get('ingreso'):
                data = RegisterAssistant(
                    name=request.user.username,  # Asegúrate de usar el nombre del usuario como cadena
                    time_in=datetime.now(),
                    time_out=None,
                    created_by=request.user,
                    updated_by=None
                )
                data.save()
                messages.success(request,"Su ingreso se registro con exito!!!..")
                return redirect('accounts:dashboard')
            else:
                try:
                    now = timezone.now()  
                    instancia = RegisterAssistant.objects.get(date_created=now, name=request.user.username)  
                    
                    instancia.time_out = datetime.now()
                    instancia.updated_by = request.user
                    instancia.date_updated = timezone.now() 
                    instancia.save()

                    messages.success(request,"SU SALIDA SE REGISTRO CON EXITO")
                    return redirect('accounts:dashboard')
                except RegisterAssistant.DoesNotExist:
                    print("No se encontro un registro")

        return render(request,"dash/register_asisten.html",context)
            
    except:
        messages.success(request,"ESTA OCURRIENDO UN ERROR COMUNICATE CON EL AREA DE SOPORTE")
        return redirect('accounts:dashboard')

from django.contrib.auth.models import User , Group

@login_required()
def listUser(request):
    context = identify_role(request)
    users_ = User.objects.exclude(username=request.user.username)
    context.update({
        'mensaje':"Verifique la lista de colaboradores",
        'users_' : users_
        })
    return render(request,"dash/list_users.html",context)

# asignar actividades por grupos exitentes
# asignar activdades directas a cada usuario

def listGroups(request):
    context = identify_role(request)
    grops_ = Group.objects.all()
    print(grops_)
    context.update({
        'mensaje':", usted podra asignar actividades a cada grupo...",
        'grops_' : grops_
        })
    return render(request,"dash/lists_groups.html",context)

from .form import RegistroActivityForm
from .models import RegistroActivity

def assignActivity(request):
    context = identify_role(request)
    mensaje = ", por favor asigna actividades para trabajo diario o semanal"
    if request.method == 'POST':
        form = RegistroActivityForm(request.POST)
        if form.is_valid():
            registro_activity = form.save(commit=False)
            registro_activity.created_by = request.user
            registro_activity.save()
            messages.success(request,"SE AGREGO CON EXITO LA ACTIVIDAD, CONTINUEMOS...")
            return redirect('dashboard:assignActivity')  
    else:
        form = RegistroActivityForm()

    context.update({'mensaje':mensaje , 'form':form})
    return render(request,"dash/assign_activity.html",context)

def listActivitys(request):
    context = identify_role(request)
    mensaje = ", podrás ver la lista de actividades "
    estado = False
    if request.method == "POST":
        start = request.POST.get('start')
        end = request.POST.get('end')
        if start and end :
            if end > start :
                print(f'llegamos diego -> {start} - {end}')
            else:
                messages.success(request,"Por favor seleccina un rango de fechas valido")
        else:
            messages.success(request,"Por favor seleccina un rango de fechas valido")
        form = RegistroActivity.objects.filter(status=True)
    else:
        form = RegistroActivity.objects.all()



    context.update({'mensaje':mensaje , 'form':form })
    return render(request,"dash/list_activity.html",context) 
# lista todas las actividades - ok 
# validar por fechas - 
# validar por estado