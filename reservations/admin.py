from django.contrib import admin
from reservations.models.customuser_models import CustomUser
from reservations.models.reservation_models import Reservation
from reservations.models.workspace_models import Workspace
from reservations.models.notification_models import Notificacion
from reservations.models.useractivitylog_models import UserActivityLog
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Workspace)
admin.site.register(Reservation)
admin.site.register(Notificacion)


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    list_filter = ('timestamp', 'user')
