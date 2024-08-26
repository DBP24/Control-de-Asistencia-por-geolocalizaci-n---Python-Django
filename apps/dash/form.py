from django import forms
from .models import RegistroActivity 

class RegistroActivityForm(forms.ModelForm):
    class Meta:
        model = RegistroActivity
        fields = ['name', 'description', 'group', 'users', 'delivery_date']  # Excluye campos creados y actualizados
        labels = {
            'name': 'Nombre de Actividad',
            'description': 'Descripción de Actividad',
            'group': 'Selecciona el Grupo',
            'delivery_date': 'Fecha de entrega',
            'users': 'Los Usuarios apareceran al seleccionar algún Grupo',
        }
      
    # Opcional: Personaliza el widget para mejorar la experiencia del usuario
    delivery_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    
    def __init__(self, *args, **kwargs):
        selected_group = kwargs.pop('selected_group', None)
        super().__init__(*args, **kwargs)

        if selected_group:
            self.fields['users'].queryset = selected_group.users.all()
      

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            })
         
class EditRegistroActivityForm(forms.ModelForm):
    class Meta:
        model = RegistroActivity
        fields = ['name', 'description', 'group', 'users', 'delivery_date']  # Excluye campos creados y actualizados
        labels = {
            'name': 'Nombre de Actividad',
            'description': 'Descripción de Actividad',
            'group': 'Selecciona el Grupo',
            'delivery_date': 'Fecha de entrega',
            'users': 'Los Usuarios apareceran al seleccionar algún Grupo',
        }
      
    # Opcional: Personaliza el widget para mejorar la experiencia del usuario
    delivery_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    
    def __init__(self, *args, **kwargs):
        selected_group = kwargs.pop('selected_group', None)
        super().__init__(*args, **kwargs)

        if selected_group:
            self.fields['users'].queryset = selected_group.users.all()
      

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
            })
        

    

