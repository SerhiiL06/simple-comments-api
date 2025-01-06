from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from src.users.serializers import RegisterUserSerializer
from rest_framework.permissions import AllowAny


class UserViewset(viewsets.ModelViewSet):
    http_method_names = ["post"]
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(**serializer.validated_data)
        return Response({"id": user.id}, status=status.HTTP_201_CREATED)
