from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.store, name='store'), #pagina principal de la tienda
    path('cart/', views.cart, name='cart'), #carro de compras
    path('checkout/', views.checkout, name='checkout'), #pago o compra
    path('form/', views.form, name='form'), #formulario
    path('login/', views.login, name='login'), #login
    
    path('clientes/', views.lista_clientes, name='clientes'),#lista clientes
    path('cliente/<int:pk>/update', views.clienteUpdateView,name='editar_cliente'),#editar clientes
    path('cliente/<int:pk>/eliminar',views.clienteEliminarView, name='eliminar_cliente'),#eliminar cleinte
    
    path('productos/', views.ProductoListView.as_view(), name="productos"),
    path('producto/add/', views.ProductoCreateView.as_view(), name="producto-add"),
    path('producto/<int:pk>/update/', views.ProductoUpdateView.as_view(), name="producto-update"),
    path('producto/<int:pk>/delete/', views.ProductoDeleteView.as_view(), name="producto-delete"),

]