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

    context = {"seleccionados": seleccionados}

    return render(request, 'store/store.html', context)


def cart(request):

    context = {}

    return render(request, 'store/cart.html', context)


def checkout(request):

    context = {}

    return render(request, 'store/checkout.html', context)


def form(request):

    context = {}

    return render(request, 'store/form.html', context)


def login(request):

    context = {}

    return render(request, 'store/login.html', context)
