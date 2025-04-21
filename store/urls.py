from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.store, name='store'), #pagina principal de la tienda
    path('cart/', views.cart, name='cart'), #carro de compras
    path('checkout/', views.checkout, name='checkout'), #pago o compra
    path('form/', views.form, name='form'), #formulario
    path('login/', views.login, name='login'), #login
]