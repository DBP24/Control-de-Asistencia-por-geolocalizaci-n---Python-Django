from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import *
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy    
from django.contrib import messages
from cvexpert.utils import limpiar_messages

from dotenv import load_dotenv
import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from .models import ResetPasswordToken
from django.contrib.sites.shortcuts import get_current_site

from django.contrib.auth import get_user_model




class UserLoginView(LoginView):
  template_name = 'accounts/login.html'
  form_class = LoginForm

  def dispatch(self, request, *args, **kwargs): 
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('accounts:dashboard'))
        return super().dispatch(request, *args, **kwargs) 

@login_required
def dashboard(request):
    limpiar_messages(request,messages)
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
      print(dash_group)

      return render(request,'dash/dashboard.html', context)

    else:
      logout(request)
      messages.success(request,"Usted no cuenta con permisos para acceder")
      return redirect('/accounts')
      
    

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print('Account created successfully!')
      return redirect('/accounts/login/')
    else:
      print("Register failed!")
  else:
    form = RegistrationForm()

  context = { 'form': form }
  return render(request, 'accounts/register.html', context)

@login_required
def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

@login_required
def update_profile(request):
   name_funtion = 'Actualizar tus Datos'
   limpiar_messages(request,messages)
   if request.method == 'POST':
      form = UserEditForm(request.POST,instance=request.user)
      if form.is_valid():
         form.save()
         messages.success(request,"Tus datos fueron actualizados con éxito")
         return redirect('accounts:dashboard')
   else:
      form = UserEditForm(instance=request.user)
   
   return render(request,'accounts/profile.html',{'form': form, 'name_funtion' : name_funtion})


from django.contrib.auth import update_session_auth_hash

def update_password(request):
  name_funtion = 'Actualiza tu contraseña'
  limpiar_messages(request, messages)
  if request.method == 'POST':
    form = EditPassUser(user=request.user, data=request.POST)
    if form.is_valid():
      user = form.save()
      update_session_auth_hash(request, user)
      messages.success(request, 'Tu contraseña ha sido cambiada con éxito.')
      return redirect('accounts:dashboard')  
    
  else:
     form = EditPassUser(user=request.user)
  
  return render ( request,'accounts/edit_pass.html',{'form':form, 'name_funtion' : name_funtion})

# envio de correo eléctronico
def forgot_password(request):
    if request.method == 'POST':
        load_dotenv()  # Carga las variables de entorno
        form = CorreoForm(request.POST)
        if form.is_valid():
            destinatario = form.cleaned_data['destinatario']
            user = get_user_model().objects.filter(email=destinatario).first()
            if user : 

              token = default_token_generator.make_token(user)
              ResetPasswordToken.objects.create(user=user, token=token)

              current_site = get_current_site(request)
              asunto = "Recupera contraseña"
              mensaje = "mensaje"
              remitente = os.getenv('USER') 

              # Envío del correo con formato HTML
              try:
                  # Renderizar el contenido HTML del archivo de plantilla
                  html_content = render_to_string('email/reset.html', {
                      'mensaje': mensaje,
                      'user' : user,
                      'domain': current_site.domain,
                      'uid': user.pk,
                      'token': token,
                      'protocol': 'http',

                  })

                  
                  # Crear el mensaje
                  email = EmailMessage(
                      subject=asunto,
                      body=html_content,
                      from_email=remitente,
                      to=[destinatario]
                  )
                  email.content_subtype = 'html'  # Importante para enviar contenido HTML
                  email.send()

                  # Limpiar el formulario después de enviar  
                  messages.success(request,"Revice su correo, e ingrese a restaurar su contraseña")
                  return redirect("accounts:login")
              except Exception as e:
                  # Manejar errores de envío de correo
                  print(f"Error al enviar el correo: {e}")  # Puedes usar un registro de errores más robusto
                  form.add_error(None, "No se pudo enviar el correo. Inténtalo nuevamente.")
            else:
              messages.error(request, "Usuario no encontrado.") 
    
    else:
        form = CorreoForm()

    return render(request, 'accounts/forgot_password.html', {'form': form})

def reset_password_confirm(request, uidb64, token):
    try:
        uid = uidb64   
        user = get_user_model().objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST['new_password']
            user.set_password(new_password)
            user.save()
            ResetPasswordToken.objects.filter(user=user).delete()
            messages.success(request, "Contraseña restablecida exitosamente.")
            return redirect('accounts:login')
        else:
            form = NewPasswordForm(request.POST)
            return render(request, 'accounts/reset_password.html', {
                'user': user,
                'token': token,
                'form' : form,
            })
    else:
        messages.error(request, "Token inválido o vencido.")
        return redirect('accounts:forgot_password')