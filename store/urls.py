from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    
    path('', views.store, name='store'), #pagina principal de la tienda
    path('cart/', views.cart, name='cart'), #carro de compras
    path('form/', views.form, name='form'), #formulario
    
    path('clientes/', views.lista_clientes, name='clientes'),#lista clientes
    path('cliente/<int:pk>/update', views.clienteUpdateView,name='editar_cliente'),#editar clientes
    path('cliente/<int:pk>/eliminar',views.clienteEliminarView, name='eliminar_cliente'),#eliminar 
    path('producto/<int:pk>/',views.detail_producto, name='detail_producto'),
    path('login/', LoginView.as_view(template_name='store/login.html'), name='login'), 
    path('api-productos/', views.fake_store_products_view, name='fake_products'), # Nueva URL para la API
    path('api-productos/<int:pk>/', views.fake_store_product_detail_view, name='fake_product_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name="update_item"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

]
