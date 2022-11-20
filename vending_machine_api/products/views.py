from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets

from .serializers import ProductSerializer
from .models import Product
from .policies import ProductAccessPolicy
# Create your views here.

'''
class ProductViewSet(ViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
'''


class ProductViewSet(
    viewsets.ModelViewSet
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ProductAccessPolicy,IsAuthenticatedOrReadOnly]
