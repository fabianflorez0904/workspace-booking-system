from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta, time

from reservations.models.customuser_models import CustomUser
from reservations.models.workspace_models import Workspace


class Reservation(models.Model):
    PENDING = 'PENDIENTE'
    CONFIRMED = 'CONFIRMADA'
    CANCELLED = 'CANCELADA'
    EXPIRED = 'EXPIRADA'

    STATUS_CHOICES = [
        (PENDING, 'Pendiente'),
        (CONFIRMED, 'Confirmada'),
        (CANCELLED, 'Cancelada'),
        (EXPIRED, 'Expirada'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    people = models.PositiveIntegerField(default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=PENDING)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Reserva de {self.user.username} en {self.workspace.name} ({self.get_status_display()})'

    def _ensure_timezone_aware(self, dt):
        """Asegura que un datetime sea timezone-aware"""
        if dt is None:
            return None
        return timezone.make_aware(dt) if dt.tzinfo is None else dt

    def can_confirm(self):
        """Verifica si la reserva puede ser confirmada"""
        now_time = timezone.now()
        start_time = self._ensure_timezone_aware(self.start_time)
        
        # Calcular ventana de confirmación (30 minutos antes hasta 15 minutos después)
        confirmation_start = start_time - timedelta(minutes=30)
        confirmation_end = start_time + timedelta(minutes=15)
        
        return (
            self.status == self.PENDING and
            confirmation_start <= now_time <= confirmation_end
        )

    def can_cancel(self):
        """Verifica si la reserva puede ser cancelada"""
        now_time = timezone.now()
        start_time = self._ensure_timezone_aware(self.start_time)
        
        return (
            self.status == self.PENDING and
            now_time < start_time
        )

    def confirm(self):
        """Confirma la reserva si está dentro del período válido"""
        if self.can_confirm():
            self.status = self.CONFIRMED
            self.confirmed_at = timezone.now()
            self.save(update_fields=['status', 'confirmed_at'])
            return True
        return False

    def cancel(self):
        """Cancela la reserva si es posible"""
        if self.can_cancel():
            self.status = self.CANCELLED
            self.cancelled_at = timezone.now()
            self.save(update_fields=['status', 'cancelled_at'])
            return True
        return False

    def validate_schedule(self):
        """Validación de horarios y reglas de negocio"""
        start_time = self._ensure_timezone_aware(self.start_time)
        end_time = self._ensure_timezone_aware(self.end_time)
        now = timezone.now()

        # Regla 1: Horario permitido (07:00 AM - 11:00 PM)
        start_hour = start_time.astimezone(timezone.get_current_timezone()).time()
        end_hour = end_time.astimezone(timezone.get_current_timezone()).time()
        
        if not (time(7, 0) <= start_hour <= time(23, 0)) or not (time(7, 0) <= end_hour <= time(23, 0)):
            raise ValidationError(
                "Las reservas solo pueden hacerse entre 07:00 AM y 11:00 PM")

        # Regla 2: Limite de anticipacion (Maximo 14 dias)
        max_reservation_date = now.date() + timedelta(days=14)
        if start_time.date() > max_reservation_date:
            raise ValidationError(
                "No puedes reservar con mas de 14 dias de anticipacion")

        # Regla 3: Duracion maxima de 8 horas
        duration = end_time - start_time
        if duration > timedelta(hours=8):
            raise ValidationError(
                "No puedes reservar un espacio por mas de 8 horas.")

    def validate_capacity(self):
        """Validación de capacidad"""
        if int(self.people) > self.workspace.capacity:
            raise ValidationError(
                "No puedes reservar el espacio porque la capacidad de personas excede la capacidad del espacio.")

    def clean(self):
        """Validacion de reglas de negocio"""
        if not self.pk or any(field in self._changed_fields for field in ['start_time', 'end_time']):
            self.validate_schedule()
        
        if not self.pk or 'people' in self._changed_fields:
            self.validate_capacity()

    def save(self, *args, **kwargs):
        # Asegurar que las fechas sean timezone-aware antes de guardar
        self.start_time = self._ensure_timezone_aware(self.start_time)
        self.end_time = self._ensure_timezone_aware(self.end_time)
        
        update_fields = kwargs.get('update_fields')
        self._changed_fields = update_fields if update_fields else None
        
        if not update_fields or any(field not in ['status', 'confirmed_at', 'cancelled_at'] for field in update_fields):
            self.clean()
        
        super().save(*args, **kwargs)
