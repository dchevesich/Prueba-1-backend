# Proyecto E-Commerce con Django y Django REST Framework

Este es un proyecto de sitio web E-Commerce desarrollado con el framework Django, ahora extendido con una **API RESTful completa** utilizando Django REST Framework. Sirve como un portafolio integral para demostrar habilidades en desarrollo backend.

## Características Principales

*   **API RESTful Completa para Productos:**
    *   Implementación de operaciones **CRUD (Crear, Leer, Actualizar, Borrar)** para el modelo `Producto`.
    *   Utilización de **Vistas Genéricas** de DRF (`ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`) para un código eficiente y escalable.
    *   Manejo de relaciones entre modelos (`Producto` y `Categoría`) a través de **Serializers**.
    *   **Seguridad Robusta:** Configuración de autenticación por **sesión y token**, con **permisos** (`IsAuthenticatedOrReadOnly`) para proteger las operaciones de escritura (POST, PUT, PATCH, DELETE).
    *   **Documentación Automática de la API:** Integración de `drf-spectacular` para generar una **interfaz interactiva Swagger UI**, facilitando la exploración y prueba de los endpoints.

*   **Flujo de Carrito y Checkout Funcional:**
    *   Sistema de carrito de compras basado en sesiones.
    *   Implementación de modelos de persistencia (`Order`, `OrderItem`, `ShippingAddress`) para registrar pedidos en la base de datos.
    *   Proceso de checkout que guarda la información del pedido y vacía el carrito.

*   **Gestión de Productos y Clientes:**
    *   Gestión de productos (modelos, listado, detalle).
    *   Sistema de autenticación completo (registro, inicio de sesión, cierre de sesión).
    *   Restricción de acceso a secciones protegidas (ej. lista de clientes).

*   **Integración Externa:**
    *   Consumo de API externa (Fake Store API) para mostrar productos adicionales.

*   **Tecnologías y Buenas Prácticas:**
    *   Desarrollado con **Django** y **Django REST Framework**.
    *   Estructura de proyecto organizada con separación de vistas de API (`store/api.py`).
    *   Diseño responsivo y estilizado con Tailwind CSS.

## Dependencias del Proyecto

Para que este proyecto funcione correctamente, es necesario instalar las siguientes dependencias:

### 1. Dependencias de Python

Las dependencias de Python están listadas en el archivo `requirements.txt`.

**Instalación:**
Se recomienda crear y activar un entorno virtual antes de instalar las dependencias.

```bash
# 1. Crear un entorno virtual (una sola vez)
python -m venv venv

# 2. Activar el entorno virtual
# En Windows:
.\venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# 3. Instalar las dependencias
pip install -r requirements.txt
```

## Cómo Ejecutar el Proyecto

1.  **Configurar la Base de Datos:**
    ```bash
    python manage.py migrate
    ```
2.  **Crear un Superusuario (para acceder al Admin y probar la API):**
    ```bash
    python manage.py createsuperuser
    ```
3.  **Iniciar el Servidor de Desarrollo:**
    ```bash
    python manage.py runserver
    ```

## Explorar la Aplicación

*   **Sitio Web E-Commerce:** Abre tu navegador y visita `http://127.0.0.1:8000/store/`.
*   **Panel de Administración:** Accede a `http://127.0.0.1:8000/admin/` con tu superusuario.
*   **Documentación Interactiva de la API (Swagger UI):** Explora los endpoints de la API en `http://127.0.0.1:8000/api/schema/swagger-ui/`.

---
