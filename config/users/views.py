from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
    RegisterSerializer
)


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({'user':UserSerializer(user).data,
                             'refresh':str(refresh),
                             'access':str(refresh.access_token),
                             'message':'User Created Successfully!'
                             }, status=status.HTTP_201_CREATED)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class LogoutView(generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({
                "message":"Refresh Token is required!"
            },status=status.HTTP_400_BAD_REQUEST
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "message":"Successfully logged out!"
            },status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response({
                'error':'invalid token'
            },status =status.HTTP_400_BAD_REQUEST
            )
