from rest_framework import viewsets
from django.contrib.auth.models import User
from src.users.serializers import RegisterUserSerializer


class UserViewset(viewsets.ModelViewSet):
    http_method_names = ["POST"]
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
