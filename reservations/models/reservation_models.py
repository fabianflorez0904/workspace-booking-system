from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta, time

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
    people = models.PositiveIntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f'Reserva de {self.user.username} en {self.workspace.name} ({self.get_status_display()})'

    def clean(self):
        """Validacion de reglas de negocio"""
        # Regla 1: Horario permitido (07:00 AM - 11:00 PM)
        start_hour = self.start_time.time()
        end_hour = self.end_time.time()
        if not (time(7, 0) <= start_hour <= time(23, 0)) or not (time(7, 0) <= end_hour <= time(23, 0)):
            raise ValidationError(
                "Las reservas solo pueden hacerse entre 07:00 AM y 11:00 PM")

        # Regla 2: Limite de anticipacion (Maximo 14 dias)
        max_reservation_date = now().date() + timedelta(days=14)
        if self.start_time.date() > max_reservation_date:
            raise ValidationError(
                "No puedes reservar con mas de 14 dias de anticipacion")

        # Regla 3: Duracion maxima de 8 horas
        duration = self.end_time - self.start_time
        if duration > timedelta(hours=8):
            raise ValidationError(
                "No puedes reservar un espacio por mas de 8 horas.")

        # Regla 4: Cantidad de personas
        capacidad_espacio = self.workspace.capacity
        if int(self.people) > capacidad_espacio:
            raise ValidationError(
                "No puedes reservar el espacio por que la capacida de personas excede la capacida del espacio.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
