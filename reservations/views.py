from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from .forms import RegistroUsuarioForm, RegistroUsuarioByAdmin, EditarUsuarioFormByAdmin, EditarUsuarioForm, CambiarPasswordForm
from .models import CustomUser
from .utils import log_activity
import json

# Create your views here.


def admin_required(view_func):
    """ Decorador de restriccion de acceso a superusuarios y administradores """
    return login_required(user_passes_test(lambda u: u.is_superuser or u.role == 'admin')(view_func))


@login_required
@admin_required
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


@login_required
@admin_required
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


def registrar_usuario(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()  # 🔥 Aquí ya usará CustomUser
            login(request, user)
            log_activity(
                request.user, f"{user.username} registro su usuario correctamente")
            return redirect('dashboard')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'usuarios/registrar.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'reservation/dashboard.html')


@login_required
@admin_required
def lista_usuarios(request):
    query = request.GET.get('q', '')
    filtro_rol = request.GET.get('rol', '')
    filtro_estado = request.GET.get('estado', '')

    usuarios = CustomUser.objects.all()

    if query:
        usuarios = usuarios.filter(
            username__icontains=query) | usuarios.filter(email__icontains=query)

    if filtro_rol:
        usuarios = usuarios.filter(role=filtro_rol)

    if filtro_estado:
        estado = True if filtro_estado == 'activo' else False
        usuarios = usuarios.filter(is_active=estado)

    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})


@login_required
@admin_required
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


@login_required
def editar_usuario(request, user_id):

    if request.user.id == user_id:
        user = get_object_or_404(CustomUser, id=user_id)

        if request.method == 'POST':
            form = EditarUsuarioForm(request.POST, instance=user)
            if form.is_valid():
                user = form.save()
                user.save()
                log_activity(request.user, f"Edito el usuario {user.username}")
                return redirect('perfil_usuario', user_id)
        else:
            form = EditarUsuarioForm(instance=user)
    else:
        return redirect('dashboard')


@login_required
def perfil_usuario(request, user_id):
    if request.user.id == user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        return redirect('dashboard')

    return render(request, 'usuarios/perfil.html', {'usuario': user})

    return render(request, 'usuarios/editar_perfil.html', {'form': form, 'usuario': user})


@login_required
def cambiar_password(request):
    if request.method == "POST":
        form = CambiarPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request, "Tu contraseña ha sido actualizada correctamente.")
            # print("Hlaaaaa La contrasena cambio")
            log_activity(request.user, f"Cambio la password")
            return redirect(reverse('perfil_usuario', kwargs={"user_id": request.user.id}))
    else:
        form = CambiarPasswordForm(user=request.user)

    return render(request, "usuarios/cambiar_password.html", {'form': form})
