from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from django.urls import reverse
from reservations.forms import EditarUsuarioForm, CambiarPasswordForm
from reservations.models import CustomUser
from reservations.utils import log_activity

# Create your views here.


@login_required
def dashboard(request):
    return render(request, 'reservation/dashboard.html')


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

    return render(request, 'usuarios/editar_perfil.html', {'form': form, 'usuario': user})


@login_required
def perfil_usuario(request, user_id):
    if request.user.id == user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        return redirect('dashboard')

    return render(request, 'usuarios/perfil.html', {'usuario': user})


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
