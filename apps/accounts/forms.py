import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class LoginForm(AuthenticationForm):
  username = UsernameField(
      widget=forms.TextInput(attrs={"class": "w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker", "placeholder": "Usuario"}),
      error_messages={
            'required': _("El campo de usuario es obligatorio."),
        }
      )
  password = forms.CharField(
      strip=False,
      widget=forms.PasswordInput(attrs={"class": "w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker", "placeholder": "Contraseña"}),
      error_messages={
        'required': 'El campo de contraseña es obligatorio',
        'min_length': 'La contraseña debe tener al menos %(limit_value)d caracteres'
    },
    min_length=3
  )

  error_messages = {
        'invalid_login': "Las credenciales que has proporcionado no son válidas. Por favor, inténtalo de nuevo.",
        'inactive': _("Esta cuenta está inactiva."),
    }
  
  # def clean_username(self):
  #       username = self.cleaned_data['username']
  #       if not re.match(r'^[a-zA-Z0-9]+$', username):
  #           raise forms.ValidationError(_("El nombre de usuario solo puede contener letras y números."))
  #       return username

  # def clean_password(self):
  #   password = self.cleaned_data['password']
  #   if not re.match(r'^[a-zA-Z0-9]+$', password):
  #      raise forms.ValidationError(_("La contraseña solo puede contener letras y números."))
  #   return password
  
class RegistrationForm(UserCreationForm):
  first_name = forms.CharField(
      max_length=30,
      required=True,
      widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker','placeholder': 'Nombres'}),
      label=_("Nombres")
    )
  last_name = forms.CharField(
      max_length=30,
      required=True,
      widget=forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker','placeholder': 'Apellidos'}),
      label=_("Apellidos")
    )
  password1 = forms.CharField(
      label=_("Password"),
      widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker','placeholder': 'Contraseña'}),
  )
  password2 = forms.CharField(
      label=_("Password Confirmation"),
      widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker','placeholder': 'Repite tu contraseña'}),
  )

  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    widgets = {
      'username': forms.TextInput(attrs={
          'class': 'w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker',
          'placeholder': 'Nombre de Usuario'
      }),
      'email': forms.EmailInput(attrs={
          'class': 'w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker',
           'placeholder': 'Email'
      })
    }


class UserEditForm(forms.ModelForm):
  class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        # fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            # 'is_active': 'Activo',
            # 'is_staff': 'Staff',
            # 'is_superuser': 'Superusuario',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
            'first_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
            'last_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
            'email': forms.EmailInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
        }

class EditPassUser(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            
        }), label='Contraseña Antigua'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
           
        }), label='Nueva Contraseña'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500',
            
        }), label='Repita su nueva contraseña'
    )

class CorreoForm(forms.Form):
    destinatario = forms.EmailField(label="Correo electrónico", widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker', 'placeholder': 'Ingrese el correo electrónico'}))
    # asunto_choices = [
    #     ('solicitar_token', 'Solicitar Token'),
    #     ('desarrollo_aplicativo', 'Desarrollo Aplicativo'),
    #     ('otros', 'Otros'),
    # ]
    # asunto = forms.ChoiceField(choices=asunto_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    # mensaje = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Ingrese el mensaje'}))

class NewPasswordForm(forms.Form):
    new_password = forms.CharField(
       widget=forms.PasswordInput(
          attrs={'class': 'w-full px-4 py-2 border rounded-md dark:bg-darker dark:border-gray-700 focus:outline-none focus:ring focus:ring-primary-100 dark:focus:ring-primary-darker', 'placeholder': 'Ingresa tu nueva contraseña'}
             ),label="Nueva Contraseña")
   
   