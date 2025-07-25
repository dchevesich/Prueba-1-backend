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
    precio = models.IntegerField(null=True, help_text="Precio")
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
    