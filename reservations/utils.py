from .models import UserActivityLog


def log_activity(user, action):
    """Registra una accion en la base de datos"""
    UserActivityLog.objects.create(user=user, action=action)
