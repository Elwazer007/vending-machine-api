from django.contrib import auth
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import RegisterSerializer, AccountDepositSerializer, UserSerializer
from .policies import UserAccessPolicy
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, status

User = get_user_model()
# Create your views here.


class SignUpAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user)
        return Response({"token": token[1]})


class UsersViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserAccessPolicy]

    @action(detail=False, methods=["patch"], serializer_class=AccountDepositSerializer)
    def deposit(self, request, pk=None):
        serializer = self.get_serializer(
            request.user, data=request.data, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = UserSerializer(request.user).data

        return Response(data=user_data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["patch"], serializer_class=None)
    def reset(self, request, pk=None):
        user = request.user
        user.deposit = 0
        user.save()
        user_data = UserSerializer(user).data
        return Response(data=user_data, status=status.HTTP_201_CREATED)
