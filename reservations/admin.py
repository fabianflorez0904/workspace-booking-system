from django.contrib import admin
from .models import CustomUser, Reservation, Workspace, Notificacion, UserActivityLog
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Workspace)
admin.site.register(Reservation)
admin.site.register(Notificacion)


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    list_filter = ('timestamp', 'user')
