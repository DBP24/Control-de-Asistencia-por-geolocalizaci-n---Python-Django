from django.contrib import admin
from .models import RegisterAssistant,RegistroActivity

class RegisterAssistantAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de administración
    list_display = ('name', 'time_in', 'time_out', 'created_at', 'updated_at', 'created_by', 'updated_by','date_created')
    
    # Campos que se pueden filtrar en la lista de administración
    list_filter = ('created_at', 'updated_at', 'created_by', 'updated_by','date_created')
    
    # Campos que se pueden buscar en la lista de administración
    search_fields = ('name',)
    
    # Campos que se mostrarán en el formulario de administración
    fields = ('name', 'time_in', 'time_out', 'created_at', 'updated_at', 'created_by', 'updated_by')
    
    # Campos que se pueden editar en el formulario de administración
    readonly_fields = ('created_at', 'updated_at', 'created_by', 'updated_by')

    # Opcional: Ordenar los registros por fecha de creación de forma descendente
    ordering = ('-created_at',)

    # Opcional: Hacer los campos de 'created_at' y 'updated_at' visibles en el formulario de edición
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('created_by', 'updated_by')
        return self.readonly_fields

    # Opcional: Establecer los campos de 'created_by' y 'updated_by' automáticamente
    def save_model(self, request, obj, form, change):
        if not change:  # If it's a new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(RegisterAssistant, RegisterAssistantAdmin)


class RegistroActivityAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de administración
    list_display = ('name', 'description', 'group')

admin.site.register(RegistroActivity, RegistroActivityAdmin)