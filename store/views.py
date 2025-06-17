from django.shortcuts import render, redirect 
from .models import Cliente 
from django.contrib import messages 
import random

# Create your views here.


def store(request):
    productos = [
        {"imagen": "images/1.jpg", "precio": 100},
        {"imagen": "images/2.jpg", "precio": 200},
        {"imagen": "images/3.jpg", "precio": 300},
    ]

    seleccionados = random.sample(productos, 3)

    reseñas = [
        {"reseña": "Muy buen producto!"},
        {"reseña": "Excelente!"},
        {"reseña": "Bueno"},

    ]
    reseña_aleatoria = random.choice(reseñas)
    context = {"seleccionados": seleccionados, "reseñas": reseña_aleatoria}

    return render(request, 'store/store.html', context)


def cart(request):

    return render(request, 'store/cart.html')


def checkout(request):

    return render(request, 'store/checkout.html')


def form(request):
    # Esta parte se ejecuta cuando el formulario es enviado (método POST)
    if request.method == 'POST':
        # 1. Obtener los datos del formulario desde request.POST
        full_name_from_html = request.POST.get('fullName')
        email_from_html = request.POST.get('email')
        address_from_html = request.POST.get('address')
        dob_from_html = request.POST.get('dob') # Fecha de Nacimiento
        phone_from_html = request.POST.get('phone')
        


        # 2. Realizar una validación básica de los campos obligatorios
        if not full_name_from_html or not email_from_html:
            messages.error(request, 'Por favor, asegúrate de completar el Nombre Completo y el Correo Electrónico.')
            # Si hay error, volvemos a mostrar el formulario sin redirigir
            return render(request, 'store/form.html')
        
        dob_for_model = dob_from_html if dob_from_html else None # Convierte '' a None para la fecha
        address_for_model = address_from_html if address_from_html else None
        phone_for_model = phone_from_html if phone_from_html else None
      

        try:
            # 4. Crear y guardar el cliente en la base de datos
            Cliente.objects.create(
                full_name=full_name_from_html,
                email=email_from_html,
                address=address_for_model,
                dob=dob_for_model,
                phone=phone_for_model,
               
            )
            
            
            messages.success(request, '¡Tu información ha sido registrada exitosamente!')
            return redirect('form_exito') 

        except Exception as e:
            # 6. Capturar cualquier error inesperado al guardar en la base de datos
            messages.error(request, f'Ocurrió un error al registrar tu información: {e}')
            return render(request, 'store/form.html')

    return render(request, 'store/form.html')


def login(request):

    context = {"bienvenido": "Ingresa tu cuenta"}
    return render(request, 'store/login.html', context)
