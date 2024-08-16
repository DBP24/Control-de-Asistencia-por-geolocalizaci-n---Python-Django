def limpiar_messages(request, messages):
    if messages.get_messages(request):
    # Itera sobre los mensajes y los elimina de la cola
        for message in messages.get_messages(request):
            pass 

# identific rol
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import  redirect

def identify_role(request):
    group = request.user.groups.all()
    if group.exists():
       group = group.first()
    else:
       group = "Super Administrador"

    if hasattr(request.user, 'groups'):
      if request.user.is_superuser:
        dash_group = "is_superuser"
      
      elif request.user.groups.filter(name = "Administrador").exists():
        dash_group = "Administrador"
      
      elif request.user.groups.exclude(name = "Administrador").exists():
        dash_group = "usuario"
      
      elif not request.user.groups.exists():
        messages.success(request,"Aún no se le asigna el grupo de trabajo")
        logout(request)
        return redirect('/accounts/login')
      
      context = {
        'name_funtion' : f'Grupo - {group}',
        'group' : dash_group
      }
   
      return context

    else:
      logout(request)
      messages.success(request,"Usted no cuenta con permisos para acceder")
      return redirect('/accounts')