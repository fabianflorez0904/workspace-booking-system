from django.urls import path
from reservations.views.user_view import dashboard, perfil_usuario, editar_usuario, cambiar_password
from reservations.views.administrador_view import registrar_usuario_admin_mode, editar_usuario_admin_mode, lista_usuarios, toggle_usuario, admin_dashboard
from reservations.views.workspace_view import lista_espacios, registrar_espacio, editar_espacio
from reservations.views.auth_view import registrar_usuario
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('usuario/perfil/<int:user_id>', perfil_usuario, name='perfil_usuario'),
    path('usuario/perfil/editar/<int:user_id>',
         editar_usuario, name='editar_usuario'),
    path('usuario/perfil/cambiarpassword/',
         cambiar_password, name='cambiar_password'),


    path('administrador/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('administrador/espacios/', lista_espacios, name='lista_espacios'),
    path('administrador/espacios/registrar',
         registrar_espacio, name='registrar_espacio'),
    path('administrador/espacios/editar/<int:espacio_id>',
         editar_espacio, name='editar_espacio'),

    path('administrador/usuarios/',
         lista_usuarios, name='lista_usuarios'),
    path('administrador/usuarios/toggle/<int:user_id>',
         toggle_usuario, name='toggle_usuario'),
    path('administrador/usuarios/registrar/',
         registrar_usuario_admin_mode, name='registrar_usuario_admin_mode'),
    path('administrador/usuarios/editar/<int:user_id>',
         editar_usuario_admin_mode, name='editar_usuario_admin_mode'),

    path('registrar/', registrar_usuario, name='registrar_usuario'),
    path('login/', auth_views.LoginView.as_view(
        template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
