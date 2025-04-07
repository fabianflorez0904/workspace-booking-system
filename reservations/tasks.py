from django.utils.timezone import now
from datetime import timedelta
from celery import shared_task
from reservations.models import Reservation


@shared_task
def update_reservation_statuses():
    """
    Tarea periódica que actualiza los estados de las reservas basado en el tiempo:
    - Cancela las reservas no confirmadas cuando pasa el tiempo de confirmación
    - Marca como expiradas las reservas que ya pasaron
    """
    current_time = now()
    updates = {
        'cancelled': 0,
        'expired': 0
    }

    # Cancelar reservas no confirmadas
    pending_reservations = Reservation.objects.filter(
        status=Reservation.PENDING,
        start_time__lte=current_time + timedelta(minutes=15)
    )
    
    for reservation in pending_reservations:
        if not reservation.can_confirm():
            reservation.status = Reservation.CANCELLED
            reservation.cancelled_at = current_time
            reservation.save()
            updates['cancelled'] += 1

    # Marcar como expiradas las reservas pasadas
    active_reservations = Reservation.objects.filter(
        status__in=[Reservation.CONFIRMED, Reservation.PENDING],
        end_time__lt=current_time
    )
    
    for reservation in active_reservations:
        reservation.status = Reservation.EXPIRED
        reservation.save()
        updates['expired'] += 1

    return f"Actualizadas {updates['cancelled']} reservas canceladas y {updates['expired']} expiradas" 