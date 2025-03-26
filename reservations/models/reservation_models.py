from django.db import models

from reservations.models.customuser_models import CustomUser
from reservations.models.workspace_models import Workspace


class Reservation(models.Model):
    PENDING = 'PENDIENTE'
    CONFIRMED = 'CONFIRMADA'
    CANCELLED = 'CANCELADA'

    STATUS_CHOICES = [
        (PENDING, 'Pendiente'),
        (CONFIRMED, 'Confirmada'),
        (CANCELLED, 'Cancelada'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f'Reserva de {self.user.username} en {self.workspace.name} ({self.get_status_display()})'
