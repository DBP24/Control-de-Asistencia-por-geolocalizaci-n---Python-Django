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
  
import os
import qrcode
from django.conf import settings
from django.core.files import File

def generate_qr_code(user):
    # Configura la ruta del archivo en el directorio estático
    qr_codes_dir = os.path.join(settings.GENERATED_FILES_DIR)
    os.makedirs(qr_codes_dir, exist_ok=True)  # Crea el directorio si no existe

    # Crea un nombre de archivo único basado en el ID del usuario
    file_name = f'user_{user}.png'
    file_path = os.path.join(qr_codes_dir, file_name)

    # Datos para el código QR
    data = f'Usuario: {user}'

    # Genera el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Crea una imagen del código QR
    img = qr.make_image(fill='black', back_color='white')

    # Guarda la imagen en el archivo especificado
    img.save(file_path)

    return file_path

