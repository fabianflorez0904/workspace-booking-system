from django.db import models
from django.utils.timezone import now
from reservations.models.customuser_models import CustomUser


class UserActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
