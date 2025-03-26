from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json


from reservations.forms.customuser_forms import RegistroUsuarioByAdmin, EditarUsuarioFormByAdmin
from reservations.utils import log_activity, require_role
from reservations.models.customuser_models import CustomUser


@require_role
def admin_dashboard(request):
    return render(request, 'reservation/admin_dashboard.html')


@require_role
def registrar_usuario_admin_mode(request):
    """Registra usuarios desde el panel de administrador"""
    if request.method == "POST":
        form = RegistroUsuarioByAdmin(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            log_activity(request.user, f"Creo el usuario {user.username}")
            return redirect('lista_usuarios')
    else:
        form = RegistroUsuarioByAdmin()

    return render(request, 'usuarios/registrobyadmin.html', {'form': form})


@require_role
def editar_usuario_admin_mode(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        form = EditarUsuarioFormByAdmin(request.POST, instance=user)
        if form.is_valid():
            form.save()
            log_activity(request.user, f"Edito el usuario {user.username}")
            return redirect('lista_usuarios')

    else:
        form = EditarUsuarioFormByAdmin(instance=user)

    return render(request, 'usuarios/edicionbyadmin.html', {'form': form, 'usuario': user})


@require_role
def lista_usuarios(request):
    query = request.GET.get('q', '')
    filtro_rol = request.GET.get('rol', '')
    filtro_estado = request.GET.get('estado', '')

    usuarios = CustomUser.objects.all()

    if query:
        usuarios = usuarios.filter(
            username__icontains=query) | usuarios.filter(email__icontains=query) | usuarios.filter(first_name__icontains=query) | usuarios.filter(last_name__icontains=query)

    if filtro_rol:
        usuarios = usuarios.filter(role=filtro_rol)

    if filtro_estado:
        estado = True if filtro_estado == 'activo' else False
        usuarios = usuarios.filter(is_active=estado)

    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})


@require_role
@csrf_exempt
def toggle_usuario(request, user_id):
    if request.method == "POST":
        usuario = get_object_or_404(CustomUser, id=user_id)

        # Evitar que un usuario se desactive a sí mismo
        if request.user == usuario:
            return JsonResponse({"success": False, "error": "No puedes desactivarte a ti mismo"}, status=400)

        data = json.loads(request.body)
        usuario.is_active = data.get("is_active", usuario.is_active)
        usuario.save()
        log_activity(
            request.user, f"Se modifico el {usuario.username} y se {'activo' if usuario.is_active else 'desactivo'}")
        return JsonResponse({"success": True, "is_active": usuario.is_active})

    return JsonResponse({"success": False}, status=400)
