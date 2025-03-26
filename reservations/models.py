from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.timezone import now

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El usuario debe tener un email")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    EMPLOYEE = 'employee'

    ROLE_CHOISES = [
        (ADMIN, 'Administrador'),
        (EMPLOYEE, 'Empleado')
    ]

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=10, choices=ROLE_CHOISES, default=EMPLOYEE)

    groups = models.ManyToManyField(
        'auth.Group', related_name="customuser_groups", blank=True)

    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name="customuser_permissions", blank=True

    )

    objects = CustomUserManager()


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


class Reservation(models.Model):
    PENDING = 'PENDIENTE'
    CONFIRMED = 'CONFIRMADA'
    CANCELLED = 'CANCELADA'

    STATUS_CHOICES = [
        (PENDING, 'Pendiente'),
        (CONFIRMED, 'Confirmada'),
        (CANCELLED, 'Cancelada'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f'Reserva de {self.user.username} en {self.workspace.name} ({self.get_status_display()})'


class Notificacion(models.Model):
    SENT = 'ENVIADO'
    PENDING = 'PENDIENTE'

    STATUS_CHOICES = [
        (SENT, 'Enviado'),
        (PENDING, 'Pendiente'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"Notificacion para {self.user.username} - {self.get_status_display()}"


class UserActivityLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
