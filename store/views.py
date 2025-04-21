from django.shortcuts import render
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

    return render(request, 'store/form.html')


def login(request):

    context = {"bienvenido": "Ingresa tu cuenta"}
    return render(request, 'store/login.html', context)
