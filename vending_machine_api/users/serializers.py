from django.contrib.auth import get_user_model

from rest_framework import serializers
from .const import ALLOWED_COINS_TO_DEPOSIT

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "role")
        extra_kwargs = {"password": {"write_only": True}, "role": {"required": True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"], role=validated_data["role"]
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "deposit", "role")
        extra_kwargs = {"deposit": {"read_only": True}}


class AccountDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["deposit"]

    def validate(self, data):

        if "deposit" not in data:
            raise serializers.ValidationError(
                "Endpoint has been called without providing deposit value"
            )
        if data["deposit"] not in ALLOWED_COINS_TO_DEPOSIT:
            raise serializers.ValidationError(
                "Endpoint has been called with invalid deposit amount value shloud be  5, 10, 20, 50 or 100."
            )
        return data

    def update(self, instance, validated_data):
        deposit_amount = validated_data["deposit"]
        new_deposit_amount = instance.deposit + deposit_amount
        instance.deposit = new_deposit_amount
        instance.save()
        return instance
