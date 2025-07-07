from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.store, name='store'), #pagina principal de la tienda
    path('cart/', views.cart, name='cart'), #carro de compras
    path('checkout/', views.checkout, name='checkout'), #pago o compra
    path('form/', views.form, name='form'), #formulario
    path('login/', views.login, name='login'), #login
    
    path('clientes/', views.lista_clientes, name='clientes'),#lista clientes
    path('cliente/<int:pk>/update', views.clienteUpdateView,name='editar_cliente'),#editar clientes
    path('cliente/<int:pk>/eliminar',views.clienteEliminarView, name='eliminar_cliente'),#eliminar cleinte

]

if settings.DEBUG: # Solo sirve archivos de medios si DEBUG es True
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)