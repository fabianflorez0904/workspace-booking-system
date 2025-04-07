from reservations.models import Workspace
from reservations.models import Reservation
from reservations.models import CustomUser
from reservations.forms.workspace_forms import WorkspaceForm
from reservations.forms.reservation_forms import ReservationForm
from reservations.utils import require_role, log_activity
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from datetime import datetime


@require_role
def lista_espacios(request):
    query = request.GET.get('q', '')
    filtro_type = request.GET.get('type', '')
    filtro_availability = request.GET.get('availability', '')
    query_capacidad = request.GET.get('capacidad', '')

    espacios = Workspace.objects.all()

    if query:
        espacios = espacios.filter(
            name__icontains=query) | espacios.filter(location__icontains=query)
    if query_capacidad:
        espacios = espacios.filter(capacity__lte=int(query_capacidad))

    if filtro_type:
        espacios = espacios.filter(type=filtro_type)

    if filtro_availability:
        estado = True if filtro_availability == 'disponible' else False
        espacios = espacios.filter(availability=estado)
    # if filtro_rol:
    #     usuarios = usuarios.filter(role=filtro_rol)

    # if filtro_estado:
    #     estado = True if filtro_estado == 'activo' else False
    #     usuarios = usuarios.filter(is_active=estado)

    return render(request, 'espacios/lista.html', {'espacios': espacios})


@require_role
def registrar_espacio(request):
    if request.method == 'POST':
        form = WorkspaceForm(request.POST)
        if form.is_valid():
            espacio = form.save()
            espacio.save()
            log_activity(request.user, f"Registro el espacio {espacio.name}")
            return redirect('lista_espacios')

    else:
        form = WorkspaceForm()

    return render(request, 'espacios/registrar.html', {'form': form})


@require_role
def editar_espacio(request, espacio_id):
    espacio = get_object_or_404(Workspace, pk=espacio_id)

    if request.method == 'POST':
        form = WorkspaceForm(request.POST, instance=espacio)
        if form.is_valid():
            form.save()
            log_activity(request.user, f"Edito el espacio {espacio.name}")
            return redirect('lista_espacios')

    else:
        form = WorkspaceForm(instance=espacio)

    return render(request, 'espacios/editar.html', {'form': form, 'espacio': espacio})


@require_role
def dashboard_workspace(request, workspace_id):
    workspace = get_object_or_404(Workspace, pk=workspace_id)
    reservations = Reservation.objects.filter(workspace=workspace)
    pending_reservations = reservations.filter(status='PENDIENTE').count()
    confirm_reservations = reservations.filter(status='CONFIRMADA').count()
    cancelled_reservations = reservations.filter(status='CANCELADA').count()
    # user = CustomUser.objects.filter(user=reservations)
    return render(request, 'espacios/dashboard_espacio.html', {
        'workspace': workspace,
        'reservations': reservations,
        'pending_reservations': pending_reservations,
        'confirm_reservations': confirm_reservations,
        'cancelled_reservations': cancelled_reservations,

    })


@login_required
def check_availability(request):
    date = request.GET.get("date")
    start_time = request.GET.get("start_time")
    end_time = request.GET.get("end_time")
    people = request.GET.get("people")

    start_datetime = datetime.strptime(
        f"{date} {start_time}", "%Y-%m-%d %H:%M")
    end_datetime = datetime.strptime(
        f"{date} {end_time}", "%Y-%m-%d %H:%M")

    time = end_datetime - start_datetime
    all_workspaces = Workspace.objects.filter()
    if people.isnumeric():
        # Filtrar workspaces por capacidad
        all_workspaces = Workspace.objects.filter(
            capacity__gte=int(people), availability=True)

    # Obtener todas las reservas que se solapan con el horario solicitado
    overlapping_reservations = Reservation.objects.filter(
        start_time__lt=end_datetime,
        end_time__gt=start_datetime,
    ).exclude(status='CANCELADA')


    # IDs de espacios reservados en el horario solicitado
    reserved_workspace_ids = overlapping_reservations.values_list("workspace", flat=True)

    # Espacios disponibles (no tienen reservas en ese horario)
    available_workspaces = all_workspaces.exclude(
        id__in=reserved_workspace_ids).order_by("capacity")

    # Encontrar espacios que estarán disponibles pronto
    soon_available_workspaces = {}
    for reservation in overlapping_reservations:
        if reservation.workspace.id in reserved_workspace_ids and reservation.workspace.capacity >= int(people or 0):
            # Si el espacio estará disponible después del horario solicitado
            if reservation.end_time.replace(tzinfo=None) > start_datetime and reservation.end_time.replace(tzinfo=None) < end_datetime:
                # Usar la hora como clave para agrupar
                available_time = reservation.end_time.strftime("%H:%M")
                if available_time not in soon_available_workspaces:
                    soon_available_workspaces[available_time] = []
                
                soon_available_workspaces[available_time].append({
                    'workspace': reservation.workspace,
                    'available_from': reservation.end_time
                })

    # Ordenar los grupos por hora
    sorted_available_times = sorted(soon_available_workspaces.keys())
    grouped_workspaces = [
        {
            'time': time,
            'workspaces': soon_available_workspaces[time]
        }
        for time in sorted_available_times
    ]

    return render(request, "reservation/available_workspaces.html", {
        "available_workspaces": available_workspaces,
        "grouped_workspaces": grouped_workspaces,
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "people": people,
        "tiempo": time,
    })


@login_required
def confirm_reservation(request):
    if request.method == 'POST':
        workspace_id = request.POST.get("workspace_id")
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        people = request.POST.get("people")

        start_datetime = datetime.strptime(
            f"{date} {start_time}", "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(
            f"{date} {end_time}", "%Y-%m-%d %H:%M")

        workspace = get_object_or_404(Workspace, pk=workspace_id)

        reservation = Reservation.objects.create(
            user=request.user,
            workspace=workspace,
            start_time=start_datetime,
            end_time=end_datetime,
            people=people,
        )
        # Redirige al dashboard o resumen de reservas
        return render(request, 'reservation/info.html', {'workspace': workspace, 'reservation': reservation})


@login_required
def info_reservation(request, reserva_id):
    reserva = get_object_or_404(Reservation, pk=reserva_id)
    espacio = get_object_or_404(Workspace, pk=reserva.workspace.id)
    return render(request, 'reservation/info.html', {'workspace': espacio, 'reservation': reserva})


def lista_reservas(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'reservation/lista_reservas.html', {'reservations': reservations})


@login_required
def dashboard(request):
    # Obtener solo las reservas pendientes del usuario actual
    reservations = Reservation.objects.filter(
        user=request.user,
        status=Reservation.PENDING
    )
    
    return render(request, 'reservation/dashboard.html', {
        'reservations': reservations
    })
