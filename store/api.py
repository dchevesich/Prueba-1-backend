from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Producto
from .serializers import ProductoSerializer


# API View para listar y crear productos
class ProductoListCreateAPIView(ListCreateAPIView):
    """
    Una vista de API que permite listar todos los productos (GET)
    y crear un nuevo producto (POST).
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


# API View para ver, actualizar y eliminar un solo producto
class ProductoRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Una vista de API que permite ver los detalles de un producto (GET),
    actualizarlo (PUT/PATCH) y eliminarlo (DELETE).
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    """
    Una vista de API de solo lectura que devuelve los detalles de un solo producto en formato JSON.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    # DRF se encarga de buscar el producto por su 'pk' (clave primaria) desde la URL.
