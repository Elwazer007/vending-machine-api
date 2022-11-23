from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    ProductSerializer,
    BuyProductSerializer,
    MinimalProductSerializer,
)
from .models import Product
from .utils import get_change
from .policies import ProductAccessPolicy

import logging

logger = logging.getLogger(__name__)


class ProductViewSet(viewsets.ModelViewSet):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, ProductAccessPolicy]

    @action(detail=False, methods=["post"], serializer_class=BuyProductSerializer)
    def buy(self, request, pk=None):
        serializer = BuyProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        product = get_object_or_404(Product, pk=serializer.data["product_id"])
        try:
            amount = serializer.data["amount"]
            amount_available = product.amout_available
            total_price = amount * product.cost
            account_deposit = user.deposit
            if amount_available < amount:
                return Response(
                    {"error_message": "Product amount is out of stock"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if account_deposit < total_price:
                return Response(
                    {"error_message": "Your account deposit isnot sufficient "},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            product.amout_available = amount_available - amount

            change = account_deposit - total_price

            change_coins = get_change(change)
            product_data = MinimalProductSerializer(product).data
            user.deposit = 0
            product.save()
            user.save()

            return Response(
                data={
                    "product": product_data,
                    "total": total_price,
                    "coins_change": change_coins,
                },
                status=status.HTTP_201_CREATED,
            )
        except Exception:
            logging.exception("Error traceback while processing buy request")
            return Response(
                "An error has occurred while purchasing the product",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
