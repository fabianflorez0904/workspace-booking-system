from django.forms import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser

# Formularios

# Gestion de Usuarios


class RegistroUsuarioForm(UserCreationForm):

    class Meta:

        model = CustomUser

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]


class RegistroUsuarioByAdmin(UserCreationForm):
    class Meta:

        model = CustomUser

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'password1',
            'password2'
        ]


class EditarUsuarioFormByAdmin(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'is_active'
        ]


class EditarUsuarioForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


class CambiarPasswordForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = [
            'old_password',
            'new_password1',
            'new_password2',
        ]
