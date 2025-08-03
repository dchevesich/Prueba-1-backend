from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, verbose_name="Nombre Completo")
    email = models.EmailField(verbose_name="Correo Electrónico")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección")
    dob = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento") # 'dob' significa Date Of Birth
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono") 
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    def __str__(self):
        # Cuando veas un objeto Cliente, te mostrará su nombre completo
        return self.full_name
    
# Modelo de Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100, help_text="Nombre del Producto")
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, help_text="Precio")
    stock = models.IntegerField(null=True, help_text="Cantidad en stock")
    # Se agrega la imagen del producto.
    imagen = models.ImageField(upload_to='productos', null=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.categoria}"
    
    def get_absolute_url(self):
        return reverse("producto_detail", args=[str(self.id)])
    
# Modelo de Categoria de Producto
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, help_text="Categoría del Producto")
    
    def __str__(self):
        return f"{self.nombre}"
    
    def get_absolute_url(self):
        return reverse("categoria_detail", args=[str(self.id)])
    
# Modelo de Pedido
class Order(models.Model):
    customer = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

# Modelo de Ítem de Pedido
class OrderItem(models.Model):
    product = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.precio * self.quantity
        return total

# Modelo de Dirección de Envío
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    