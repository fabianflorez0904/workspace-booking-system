from django.urls import path
from .views import registrar_usuario
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registrar/', registrar_usuario, name='registrar_usuario'),



    path('login/', auth_views.LoginView.as_view(template_name='reservation/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
