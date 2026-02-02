from django.shortcuts import render
from .serializers import UserSerializer,RegisterSerializer,LoginSerializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from rest_framework.authtoken.models import Token
from rest_framework import generics , permissions , status

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        #create token for the user
        token, created = Token.objects.get_or_create(user=user)

        #login the user
        login(request, user)
        return Response({'user':UserSerializer(user).data,
                              'token':token.key,
                              'message':'Registration Successful!'
                         }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        #create or get token
        token , created = Token.objects.get_or_create(user=user)

        #login the user
        login(request, user)
        return Response({'user':UserSerializer(user).data,
                         'token':token.key,
                         'message':'Login Successful!'
                         })

class LogoutView(APIView):
    def post(self,request):
        # delete the token
        try:
            request.user.auth_token.delete()
        except:
            pass

        # Logout the user
        logout(request)
        return Response({'message':'Logout Successful!'})

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user