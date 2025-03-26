# 🏢 Workspace Management System

Este proyecto es una plataforma de gestión de espacios de trabajo con autenticación y administración de usuarios.

## 🚀 Características Implementadas

✅ **Autenticación de Usuarios**

- Inicio de sesión, registro y cierre de sesión con Django Auth.
- Personalización del modelo de usuario con `AbstractUser`.
- Implementación de permisos y roles (`ADMIN` y `EMPLOYEE`).

✅ **Gestión de Usuarios**

- Panel de administración con CRUD de usuarios.
- Actualización de perfiles y cambio de contraseñas.
- Logs de auditoría (`UserActivityLogs`).

✅ **Seguridad**

- Hashing de contraseñas con `pbkdf2_sha256`.
- Protección contra intentos de acceso no autorizado.

## 🛠️ Tecnologías Usadas

- **Backend**: Django (Python)
- **Base de Datos**: PostgreSQL
- **Autenticación**: Django Auth
- **Control de Versiones**: Git y GitHub

## 📦 Instalación

1. Clonar el repositorio

   ```bash
   git clone https://github.com/tu-usuario/workspace-management.git
   cd workspace-management

   ```

2. Crear un entorno virtual y activarlo

```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate

```

3. Instalar dependencias

```bash
   pip install -r requirements.txt
```
