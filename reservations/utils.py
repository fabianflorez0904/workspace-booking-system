from reservations.models.useractivitylog_models import UserActivityLog
from django.shortcuts import redirect
from functools import wraps


def log_activity(user, action):
    """Registra una accion en la base de datos"""
    UserActivityLog.objects.create(user=user, action=action)


def require_role(view_func):
    """Decorador para restringir vistar segun el rol de usuario"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.role == 'admin' or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        return redirect('dashboard')  # si no tiene permiso retornamos
    return wrapper
