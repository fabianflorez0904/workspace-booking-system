from reservations.models import Workspace
from reservations.forms.workspace_forms import WorkspaceForm
from reservations.utils import require_role, log_activity
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404


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
