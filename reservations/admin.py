from django.contrib import admin
from .models import CustomUser, Reservation, Workspace, Notificacion
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Workspace)
admin.site.register(Reservation)
admin.site.register(Notificacion)
