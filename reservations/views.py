from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegistroUsuarioForm
# Create your views here.


def registrar_usuario(request):
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()  # 🔥 Aquí ya usará CustomUser
            login(request, user)
            return redirect('login')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'reservation/registrar.html', {'form': form})
