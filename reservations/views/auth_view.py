
from reservations.forms import RegistroUsuarioForm
from reservations.utils import log_activity
from django.shortcuts import redirect, render
from django.contrib.auth import login


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
