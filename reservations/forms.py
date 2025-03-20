from django.forms import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser

# Formularios


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
