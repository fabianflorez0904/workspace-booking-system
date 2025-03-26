from django.db import models
from reservations.models.customuser_models import CustomUser


class Notificacion(models.Model):
    SENT = 'ENVIADO'
    PENDING = 'PENDIENTE'

    STATUS_CHOICES = [
        (SENT, 'Enviado'),
        (PENDING, 'Pendiente'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"Notificacion para {self.user.username} - {self.get_status_display()}"
