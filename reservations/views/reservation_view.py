from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.utils.timezone import now
from datetime import datetime, timedelta

from reservations.models import Reservation, Workspace
from reservations.utils import log_activity


@login_required
def confirm_attendance(request, reservation_id):
    """Vista para confirmar la asistencia a una reserva"""
    reservation = get_object_or_404(Reservation, pk=reservation_id, user=request.user)
    
    if reservation.can_confirm():
        if reservation.confirm():
            messages.success(request, "Reserva confirmada exitosamente.")
            log_activity(request.user, f"Confirmó la asistencia a la reserva {reservation.id}")
        else:
            messages.error(request, "No se pudo confirmar la reserva.")
    else:
        messages.error(request, "Esta reserva no puede ser confirmada en este momento.")
    
    return redirect('info_reservation', reserva_id=reservation_id)


@login_required
def cancel_reservation(request, reservation_id):
    """Vista para cancelar una reserva"""
    reservation = get_object_or_404(Reservation, pk=reservation_id, user=request.user)
    
    if reservation.can_cancel():
        if reservation.cancel():
            messages.success(request, "Reserva cancelada exitosamente.")
            log_activity(request.user, f"Canceló la reserva {reservation.id}")
        else:
            messages.error(request, "No se pudo cancelar la reserva.")
    else:
        messages.error(request, "Esta reserva no puede ser cancelada en este momento.")
    
    return redirect('lista_reservas')


@login_required
def lista_reservas(request):
    """Vista para listar las reservas del usuario"""
    current_time = now()
    
    # Obtener parámetros de la solicitud GET
    status_filter = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    workspace_type_filter = request.GET.get('workspace_type')

    # Filtrar reservas por estado y tiempo
    proximas_reservas = Reservation.objects.filter(user=request.user, start_time__gt=current_time)

    # Aplicar filtros según los parámetros
    if status_filter:
        if status_filter == "PENDIENTE":
            proximas_reservas = proximas_reservas.filter(status=Reservation.PENDING)
        elif status_filter == "CONFIRMADA":
            proximas_reservas = proximas_reservas.filter(status=Reservation.CONFIRMED)
        elif status_filter == "CANCELADA":
            proximas_reservas = proximas_reservas.filter(status=Reservation.CANCELLED)

    if date_from:
        proximas_reservas = proximas_reservas.filter(start_time__gte=date_from)

    if date_to:
        proximas_reservas = proximas_reservas.filter(start_time__lte=date_to)

    if workspace_type_filter:
        proximas_reservas = proximas_reservas.filter(workspace__type=workspace_type_filter)

    proximas_reservas = proximas_reservas.order_by('start_time')
    
    reservas_pasadas = Reservation.objects.filter(
        user=request.user,
        end_time__lt=current_time
    ).order_by('-start_time')
    
    reservas_canceladas = Reservation.objects.filter(
        user=request.user,
        status=Reservation.CANCELLED
    ).order_by('-start_time')
    
    context = {
        'reservations': proximas_reservas,
        'reservas_pasadas': reservas_pasadas,
        'reservas_canceladas': reservas_canceladas,
    }
    
    return render(request, 'reservation/lista_reservas.html', context)


@login_required
def info_reservation(request, reserva_id):
    """Vista detallada de una reserva"""
    reserva = get_object_or_404(Reservation, pk=reserva_id, user=request.user)
    espacio = get_object_or_404(Workspace, pk=reserva.workspace.id)
    
    # Verificar si la reserva puede ser confirmada o cancelada
    can_confirm = reserva.can_confirm()
    can_cancel = reserva.can_cancel()
    
    context = {
        'workspace': espacio,
        'reservation': reserva,
        'can_confirm': can_confirm,
        'can_cancel': can_cancel,
    }
    
    return render(request, 'reservation/info.html', context)

