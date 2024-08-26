from django.db import models
from django.conf import settings
from django.utils import timezone

class RegisterAssistant(models.Model):
    name = models.CharField(max_length=150)
    # Campos de hora
    time_in = models.TimeField(null=True, blank=True)  # Hora de ingreso
    time_out = models.TimeField(null=True, blank=True)  # Hora de salida
    
    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Campo de usuario que crea
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='register_assistants_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='register_assistants_updated'
    )
    
    date_created = models.DateField(auto_now_add=True)

from django.contrib.auth.models import  Group
from django.core.validators import MinValueValidator, MaxValueValidator

class RegistroActivity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='activities')
    delivery_date = models.DateTimeField(null=False)
    progress_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Campo de usuario que crea
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='register_activity_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='register_activity_updated'
    )

    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='register_activities')

    
    def __str__(self):
        return  f'{self.name} - {self.description}'
