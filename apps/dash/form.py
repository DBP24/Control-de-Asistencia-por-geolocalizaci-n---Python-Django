from django import forms
from .models import RegistroActivity

class RegistroActivityForm(forms.ModelForm):
    class Meta:
        model = RegistroActivity
        fields = ['name', 'description', 'group', 'delivery_date']  # Excluye campos creados y actualizados
        labels = {
            'name': 'Nombre de Actividad',
            'description': 'Descripción de Actividad',
            'group': 'Selecciona el Grupo',
            'delivery_date': 'Fecha de entrega',
            # 'is_active': 'Activo',
            # 'is_staff': 'Staff',
            # 'is_superuser': 'Superusuario',
        }
    # Opcional: Personaliza el widget para mejorar la experiencia del usuario
    delivery_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcional: Personaliza la apariencia de los campos del formulario
        self.fields['name'].widget.attrs.update({'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['description'].widget.attrs.update({'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['group'].widget.attrs.update({'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
        self.fields['delivery_date'].widget.attrs.update({'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
