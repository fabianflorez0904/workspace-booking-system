import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Establecer la configuración de Django por defecto para celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Crear la aplicación Celery
app = Celery('workspace_booking')

# Configurar usando el objeto settings de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cargar tareas automáticamente de todas las aplicaciones registradas
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Configurar tareas periódicas
app.conf.beat_schedule = {
    'update-reservation-statuses': {
        'task': 'reservations.tasks.update_reservation_statuses',
        'schedule': 60.0,  # Cada 60 segundos
    },
} 