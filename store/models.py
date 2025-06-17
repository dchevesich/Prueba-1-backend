from django.db import models

class Cliente(models.Model):
    
    full_name = models.CharField(max_length=200, verbose_name="Nombre Completo")
    email = models.EmailField(verbose_name="Correo Electrónico")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Dirección")
    dob = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento") # 'dob' significa Date Of Birth
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono") 
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    def __str__(self):
        # Cuando veas un objeto Cliente, te mostrará su nombre completo
        return self.full_name