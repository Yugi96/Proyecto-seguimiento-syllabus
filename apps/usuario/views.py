from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from apps.usuario.serializers import UserSerializer
# Create your views here.
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer