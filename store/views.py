from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Producto, Categoria, Order, OrderItem, ShippingAddress # Importar los nuevos modelos
from django.contrib import messages
import random
from django.http import JsonResponse
import json
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ClienteForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as OriginalLoginView
from django.contrib.auth import login as auth_login
# from rest_framework.generics import ListAPIView # Ya no se usa aquí
# from .serializers import ProductoSerializer # Ya no se usa aquí
import requests
import uuid # Para generar transaction_id

# Create your views here.

def store(request):
    producto_obtenidos = Producto.objects.all()
    context = {"producto": producto_obtenidos}
    return render(request, 'store/store.html', context)

def updateItem(request):
    if request.method == 'POST':
        try: # Añadimos un try-except general para capturar cualquier error
            data = json.loads(request.body)
            productId = str(data['productId'])
            action = data['action']

            print('\n--- DEBUG updateItem ---')
            print('Action:', action)
            print('Product:', productId)

            cart = request.session.get('cart', {})
            print(f"Carrito al inicio (desde sesión): {cart}")

            if productId in cart:
                if action == 'add':
                    cart[productId]['quantity'] += 1
                elif action == 'remove':
                    cart[productId]['quantity'] -= 1
            else:
                if action == 'add':
                    cart[productId] = {'quantity': 1}

            if productId in cart and cart[productId]['quantity'] <= 0:
                del cart[productId]

            request.session['cart'] = cart
            request.session.modified = True 

            print(f"Carrito después de la modificación: {cart}")
            print(f"request.session.modified: {request.session.modified}")
            print('--- FIN DEBUG updateItem ---\n')

            return JsonResponse('Item was added', safe=False)

        except Exception as e:
            # Si ocurre cualquier error dentro de la vista, lo imprimimos en la terminal
            print(f"\n--- ERROR EN updateItem ---")
            print(f"Excepción: {e}")
            import traceback
            traceback.print_exc() # Imprime el traceback completo para más detalles
            print(f"--- FIN ERROR updateItem ---\n")
            # Y devolvemos un JsonResponse con un mensaje de error HTTP 500
            return JsonResponse(f'Error procesando solicitud: {e}', status=500, safe=False)
    else:
        return JsonResponse('Method not allowed', status=405)
    
def checkout(request):
    # Lógica para GET (mostrar el carrito en el checkout)
    cart_from_session = request.session.get('cart', {})
    items = []
    order_summary = {'get_cart_total': 0, 'get_cart_items': 0}

    for product_id, item_data in cart_from_session.items():
        try:
            product = Producto.objects.get(id=product_id)
            quantity = item_data['quantity']
            total = (product.precio or 0) * quantity

            items.append({
                'product': product,
                'quantity': quantity,
                'get_total': total,
            })
            order_summary['get_cart_total'] += total
            order_summary['get_cart_items'] += quantity
        except Producto.DoesNotExist:
            print(f"DEBUG: Producto con ID {product_id} no encontrado en la base de datos para checkout.")
        except Exception as e:
            print(f"DEBUG: Error procesando ítem {product_id} en carrito para checkout: {e}")

    if request.method == 'POST':
        # Lógica para POST (procesar el pedido)
        if request.user.is_authenticated:
            customer = request.user.cliente # Asumiendo que cada User tiene un Cliente asociado
        else:
            # Manejar usuarios no autenticados si es necesario, por ahora, solo autenticados
            messages.error(request, "Debes iniciar sesión para completar el pedido.")
            return redirect('login') # O a la página de checkout de nuevo

        # Obtener datos del formulario
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        # Crear el objeto Order
        order = Order.objects.create(
            customer=customer,
            complete=False, # Por ahora, el pedido no está completo hasta que se pague
            transaction_id=str(uuid.uuid4()) # Generar un ID único para la transacción
        )

        # Crear OrderItems a partir del carrito de la sesión
        for product_id, item_data in cart_from_session.items():
            try:
                product = Producto.objects.get(id=product_id)
                quantity = item_data['quantity']
                OrderItem.objects.create(
                    product=product,
                    order=order,
                    quantity=quantity
                )
            except Producto.DoesNotExist:
                print(f"DEBUG: Producto con ID {product_id} no encontrado al crear OrderItem.")
            except Exception as e:
                print(f"DEBUG: Error al crear OrderItem para producto {product_id}: {e}")

        # Crear la dirección de envío
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
        )

        # Marcar el pedido como completo (simulando pago exitoso)
        order.complete = True
        order.save()

        # Vaciar el carrito de la sesión
        del request.session['cart']
        request.session.modified = True
        messages.success(request, "¡Tu pedido ha sido realizado con éxito!")
        return redirect('store') # Redirigir a la página principal o a una de confirmación

    # Lógica para GET (mostrar el formulario de checkout)
    context = {
        'items': items,
        'order': order_summary,
        'shipping_required': True # Puedes usar esto para mostrar/ocultar campos de envío
    }
    return render(request, 'store/checkout.html', context)


def cart(request):
    cart_from_session = request.session.get('cart', {})
    # print('\n--- DEBUG cart view ---')
    # print(f"Carrito recuperado en vista 'cart': {cart_from_session}")

    items = [] # Lista para almacenar los ítems del carrito con detalles del producto
    order = {'get_cart_total': 0, 'get_cart_items': 0} # Diccionario para almacenar el total y la cantidad de ítems

    for product_id, item_data in cart_from_session.items():
        try:
            # Obtener el objeto Producto de la base de datos de Django
            product = Producto.objects.get(id=product_id)
            quantity = item_data['quantity']

            # Calcular subtotal para este ítem
            total = (product.precio or 0) * quantity # Usar 0 si precio es None

            # Construir el diccionario para el ítem de la plantilla
            item = {
                'product': product,
                'quantity': quantity,
                'get_total': total, # Subtotal de este ítem
            }
            items.append(item)

            # Sumar al total general del carrito
            order['get_cart_total'] += total
            order['get_cart_items'] += quantity

        except Producto.DoesNotExist:
            # Si el producto no se encuentra en la DB (ej. fue borrado)
            print(f"DEBUG: Producto con ID {product_id} no encontrado en la base de datos.")
          
        except Exception as e:
            print(f"DEBUG: Error procesando ítem {product_id} en carrito: {e}")

    print(f"Ítems para plantilla: {items}")
    print(f"Order summary: {order}")
    print('--- FIN DEBUG cart view ---\n')

    context = {'items': items, 'order': order} # Pasar 'items' y 'order' a la plantilla
    return render(request, 'store/cart.html', context)


def fake_store_products_view(request):
    products = [] # Lista para almacenar los productos de la API
    error_message = None # Para manejar posibles errores

    try:
        # URL del endpoint para obtener todos los productos de la Fake Store API
        api_url = "https://fakestoreapi.com/products"

        # Realiza la solicitud HTTP GET a la API
        response = requests.get(api_url)

        # Si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            products = response.json() # Convierte la respuesta JSON a un objeto Python (lista de diccionarios)
        else:
            # Si la API devuelve un error (ej. 404, 500)
            error_message = f"Error al consumir la API: {response.status_code} - {response.text}"

    except requests.exceptions.RequestException as e:
        # Captura errores de red, conexión, timeouts, etc.
        error_message = f"Error de conexión con la API: {e}"

    except ValueError as e:
        # Captura errores si la respuesta no es un JSON válido
        error_message = f"Error al decodificar la respuesta JSON de la API: {e}"

    context = {
        'products': products, # Pasa la lista de productos a la plantilla
        'error_message': error_message # Pasa cualquier mensaje de error
    }

    return render(request, 'store/fake_store_products.html', context)

def fake_store_product_detail_view(request, pk): # La vista recibe el pk del producto
    product_detail = None
    error_message = None

    try:
        # URL del endpoint para obtener un producto específico por su ID
        api_url = f"https://fakestoreapi.com/products/{pk}"
        
        # Realiza la solicitud HTTP GET a la API
        response = requests.get(api_url)
        
        # Si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            product_detail = response.json() # Convierte la respuesta JSON a un objeto Python (diccionario)
            
      
            if not product_detail: 
                error_message = "Producto no encontrado en la Fake Store API."
                product_detail = None 

        else:
            error_message = f"Error al consumir la API: {response.status_code} - {response.text}"
    
    except requests.exceptions.RequestException as e:
        error_message = f"Error de conexión con la API: {e}"
    
    except ValueError as e:
        error_message = f"Error al decodificar la respuesta JSON de la API: {e}"

    context = {
        'product': product_detail, # Pasa el detalle del producto (o None)
        'error_message': error_message # Pasa cualquier mensaje de error
    }
    
    return render(request, 'store/fake_store_product_detail.html', context)

def form(request):
    if request.method == 'POST':
        full_name_from_html = request.POST.get('full_name')
        email_from_html = request.POST.get('email')
        address_from_html = request.POST.get('address')
        dob_from_html = request.POST.get('dob') 
        phone_from_html = request.POST.get('phone')

        if not full_name_from_html or not email_from_html:
            messages.error(request, 'Por favor, asegúrate de completar el Nombre Completo y el Correo Electrónico.')
            return render(request, 'store/form.html')
        
        dob_for_model = None
        if dob_from_html:
            try:
                dob_for_model = datetime.strptime(dob_from_html, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, 'El formato de la Fecha de Nacimiento es incorrecto. Use AAAA-MM-DD.')
                pass 
        
        try:
            Cliente.objects.create(
                full_name=full_name_from_html,
                email=email_from_html,
                address=address_from_html,
                dob=dob_for_model,
                phone=phone_from_html,
            )
            messages.success(request, '¡Tu información ha sido registrada exitosamente!')
            return redirect('clientes') 

        except Exception as e:
            messages.error(request, f'Ocurrió un error al registrar tu información: {e}')
            return render(request, 'store/form.html')

    return render(request, 'store/form.html')



# lista de clientes
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()  # obtiene todos los registros de Cliente
    
    return render(request, 'store/listaclientes.html', {'clientes': clientes})

# actualzizar cliente
def clienteUpdateView(request, pk):
    cliente_obj = get_object_or_404(Cliente, id=pk)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        dob_str = request.POST.get('dob')
        phone = request.POST.get('phone')

        dob_object = None
        if dob_str:
            try:
                dob_object = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                pass

        cliente_obj.full_name = full_name
        cliente_obj.email = email
        cliente_obj.address = address
        cliente_obj.dob = dob_object
        cliente_obj.phone = phone
        cliente_obj.save()
        return redirect('clientes')

    else:
        context = {
            'cliente': cliente_obj
        }
        return render(request, 'store/editar_cliente.html', context)
    
# eliminar cliente
def clienteEliminarView(request, pk):
    cliente_obj = get_object_or_404(Cliente,id=pk)
    cliente_obj.delete()
    return redirect(lista_clientes)


def detail_producto(request,pk):
    producto_obj = get_object_or_404(Producto, id=pk)

    context = {
        'producto':producto_obj
    }

    return render(request,"store/detalle_producto.html",context)

def form(request):
    if request.method == 'POST':
        # Instanciamos los formularios con los datos del POST
        user_form = CustomUserCreationForm(request.POST)
        cliente_form = ClienteForm(request.POST)

        # Validamos ambos formularios
        if user_form.is_valid() and cliente_form.is_valid():
            
            user = user_form.save() 
            cliente = cliente_form.save(commit=False) 
            cliente.user = user 
            cliente.email = user.email 
            cliente.save() 

            messages.success(request, '¡Tu cuenta ha sido creada exitosamente! Ya puedes iniciar sesión.')
            return redirect('login') 
        else:
            # Si alguno de los formularios no es válido, mostramos los errores
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
            # Podemos imprimir los errores en la terminal para depurar
            print(f"Errores del formulario de usuario: {user_form.errors}")
            print(f"Errores del formulario de cliente: {cliente_form.errors}")

    else: # Si el método es GET, mostramos formularios vacíos
        user_form = CustomUserCreationForm()
        cliente_form = ClienteForm()

    context = {
        'user_form': user_form,
        'cliente_form': cliente_form,
    }
    return render(request, 'store/form.html', context)




