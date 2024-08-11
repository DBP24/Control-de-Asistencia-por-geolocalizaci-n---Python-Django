from django.contrib import admin
from .models import ResetPasswordToken

@admin.register(ResetPasswordToken)
class ResetPasswordTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    search_fields = ('user__username', 'token')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)

    def has_add_permission(self, request):
        # Evitar la creación manual de tokens desde el admin
        return False

    def has_change_permission(self, request, obj=None):
        # Permitir la visualización pero no la edición
        return True

    def has_delete_permission(self, request, obj=None):
        # Evitar la eliminación desde el admin
        return False
