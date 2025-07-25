# Proyecto E-Commerce con Django

Este es un proyecto de sitio web E-Commerce desarrollado con el framework Django, como parte de la asignatura de Programación BackEnd Django.

## Características Principales

* Gestión de productos (modelos, listado, detalle).
* Sistema de autenticación completo (registro, inicio de sesión, cierre de sesión).
* Restricción de acceso a secciones protegidas (ej. lista de clientes).
* Consumo de API externa (Fake Store API) para mostrar productos.
* Carrito de compras básico (basado en sesiones).
* Diseño responsivo y estilizado con Tailwind CSS.

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