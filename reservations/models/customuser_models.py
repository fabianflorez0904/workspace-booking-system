from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


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
