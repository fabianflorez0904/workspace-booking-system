from django.db import models


class Workspace(models.Model):
    OFFICE = 'OFICINA'
    MEETING_ROOM = 'SALA_REUNIONES'
    COWORKING = 'COWORKING'

    WORKSPACE_TYPES = [
        (OFFICE, 'Oficina'),
        (MEETING_ROOM, 'Sala de Reuniones'),
        (COWORKING, 'Coworking'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=WORKSPACE_TYPES)
    capacity = models.IntegerField()
    location = models.CharField(max_length=255)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
