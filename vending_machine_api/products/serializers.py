from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "amout_available", "cost", "seller"]
        extra_kwargs = {"seller": {"required": False, "read_only": True}}

    def validate(self, data):
        if "amout_available" in data and data["amout_available"] < 0:
            raise serializers.ValidationError("Product amount shloud be >= 0")
        if "cost" in data and (data["cost"] <= 0 or data["cost"] % 5 != 0):
            raise serializers.ValidationError(
                "Product cost shloud be > 0 and divisible by 5 "
            )
        return data

    def create(self, validated_data):
        name = validated_data["name"]
        amout_available = validated_data.get("amout_available", 0)
        cost = validated_data["cost"]
        seller = self.context["request"].user
        product = Product.objects.create(
            name=name, amout_available=amout_available, cost=cost, seller=seller
        )
        return product


class BuyProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True, min_value=1)
    amount = serializers.IntegerField(required=True, min_value=1)


class MinimalProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "cost"]
