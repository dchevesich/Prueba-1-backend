from django.contrib import admin
from .models import Producto, Categoria, Cliente, Order, OrderItem, ShippingAddress # Importar los nuevos modelos

# Register your models here.
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Order) # <-- NUEVO
admin.site.register(OrderItem) # <-- NUEVO
admin.site.register(ShippingAddress) # <-- NUEVO