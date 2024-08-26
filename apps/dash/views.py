from django.shortcuts import render,get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse, JsonResponse
from cvexpert.utils import *
from django.contrib import messages
from .models import RegisterAssistant , RegistroActivity

from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User , Group
from .form import RegistroActivityForm , EditRegistroActivityForm


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

        return render(request,"dash/activitys/register_asisten.html",context)
            
    except:
        messages.success(request,"ESTA OCURRIENDO UN ERROR COMUNICATE CON EL AREA DE SOPORTE")
        return redirect('accounts:dashboard')


@login_required()
def get_users_by_group(request):
    group_id = request.GET.get('group_id')
    # print(group_id)
    users = User.objects.filter(groups__id=group_id) if group_id else []
    user_list = list(users.values('id', 'username','last_name','first_name'))  # Devuelve solo ID y username
    return JsonResponse(user_list, safe=False)

@login_required()
def listUser(request):
    context = identify_role(request)
    users_ = User.objects.exclude(username=request.user.username)
    context.update({
        'mensaje':"Verifique la lista de colaboradores",
        'users_' : users_
        })
    return render(request,"dash/activitys/list_users.html",context)

@login_required()
def listGroups(request):
    context = identify_role(request)
    grops_ = Group.objects.all()
    print(grops_)
    context.update({
        'mensaje':", usted podra asignar actividades a cada grupo...",
        'grops_' : grops_
        })
    return render(request,"dash/activitys/lists_groups.html",context)


@login_required()
def assignActivity(request):
    context = identify_role(request)
    mensaje = ", por favor asigna actividades para trabajo diario o semanal"
    if request.method == 'POST':
        form = RegistroActivityForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            registro_activity = form.save(commit=False)
            registro_activity.created_by = request.user
            registro_activity.save()
            form.save_m2m() 
            messages.success(request,"SE AGREGO CON EXITO LA ACTIVIDAD, CONTINUEMOS...")
            return redirect('dashboard:assignActivity') 
        else:
            messages.success(request,"A ocurrido un error verifica el ingreso de los datos") 
    else:
        selected_group_id = request.GET.get('group')  # Obtener el grupo seleccionado desde la URL o el contexto
        selected_group = Group.objects.filter(id=selected_group_id).first() if selected_group_id else None
        form = RegistroActivityForm(selected_group=selected_group)

    context.update({'mensaje':mensaje , 'form':form})
    return render(request,"dash/activitys/assign_activity.html",context)

@login_required()
def listActivitys(request):
    context = identify_role(request)
    mensaje = ", podrás ver la lista de actividades "
    estado = False
    if request.method == "POST":
        start = request.POST.get('start')
        end = request.POST.get('end')

        start_date = datetime.strptime(start, "%m/%d/%Y")
        end_date = datetime.strptime(end, "%m/%d/%Y")
        
        if start and end :
            if end > start :
                messages.success(request,f'Se muestra datos de las fechas {start} - {end}')
                form = RegistroActivity.objects.filter(created_at__gte=start_date,created_at__lte=end_date).order_by('-created_at')
            else:
                messages.success(request,"Por favor seleccina un rango de fechas valido")
        else:
            messages.success(request,"Por favor seleccina un rango de fechas valido")
        # form = RegistroActivity.objects.all().order_by('-created_at')
    else:
        form = RegistroActivity.objects.all().order_by('-created_at')



    context.update({'mensaje':mensaje , 'form':form })
    return render(request,"dash/activitys/list_activity.html",context) 

@login_required()
def list_activity(request,id):
    context = identify_role(request)
    mensaje = ", Verifica la información que has añadido a tu actividad"
    form = RegistroActivity.objects.get(id = id)
    for_create = form.created_by
    usuarios = [user.username for user in form.users.all()]
    create = User.objects.get(username=for_create)
    usr=[]
    for us in usuarios:
        user = User.objects.get(username=us)
        usr.append(f'{user.first_name} {user.last_name} - {user}')
        
    
    print(usr)
    context.update({'mensaje':mensaje , 'form':form , 'user':usr , 'create' : create})
    return render(request,"dash/activitys/activity.html",context) 

@login_required()
def clear_activity(request,id=None):
    context = identify_role(request)
    mensaje = ",Desear Eliminar la Actividad"
    if request.method == "POST":
        id_ = request.POST.get('delete')
        form = RegistroActivity.objects.get(id = id_)
        form.delete()
        messages.success(request, "Se a eliminado con éxito la actividad")
        return redirect('dashboard:listActivitys') 

    context.update({'mensaje':mensaje , 'id':id})
    return render(request,"dash/activitys/delete_activity.html",context) 

from datetime import datetime
@login_required()
def edit_activity(request,id=None):
    context = identify_role(request)
    mensaje = ", Actualice la informaciòn de la actividad"
    activity = get_object_or_404(RegistroActivity, id=id)
    delivery_date = activity.delivery_date
    name = activity.name
    description = activity.description
    group = activity.group
    users = activity.users.all()
    print(users)
    if request.method == "POST":
        form = EditRegistroActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, "Se actualizó con éxito la actividad")
            return redirect('dashboard:listActivitys') 
    else:
        received_date = datetime.strptime(str(delivery_date), '%Y-%m-%d %H:%M:%S')
        # print(received_date)
        # # Formatear al formato `datetime-local`
        formatted_date = received_date.strftime('%Y-%m-%dT%H:%M')

        form = EditRegistroActivityForm()
        form.fields['name'].initial = name
        form.fields['description'].initial = description
        form.fields['delivery_date'].initial = formatted_date
        form.fields['group'].initial = group
        form.fields['users'].initial = users
        
       

    context.update({'mensaje':mensaje , 'form':form })
    return render(request,"dash/activitys/edit_activity.html",context) 