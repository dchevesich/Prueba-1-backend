from rest_framework import serializers
from .models import Producto, Categoria

# Serializer para el modelo Categoria.

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre'] # Solo exponemos el id y el nombre

# Serializer para el modelo Producto
class ProductoSerializer(serializers.ModelSerializer):
    ## Metodo get
    categoria = CategoriaSerializer(read_only=True)
    ## Metodo post
    categoria_id = serializers.IntegerField(write_only=True)
    imagen = serializers.ImageField(required=False)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'stock', 'imagen', 'categoria', 'categoria_id']
