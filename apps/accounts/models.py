
from django.db import models
from django.conf import settings

class ResetPasswordToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)  # Asegura que el token sea único
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'Token for user {self.user} created at {self.created_at}'
