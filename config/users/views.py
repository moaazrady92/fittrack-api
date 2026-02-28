from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken #for generating and blacklist tokens and refresh token lives long unlike access token
from rest_framework.generics import (
    GenericAPIView,
    RetrieveUpdateAPIView ,
    CreateAPIView
)
from .serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
    RegisterSerializer
)

User = get_user_model()

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) #requisting data from serializers first
        serializer.is_valid(raise_exception=True)
        user = serializer.save() #saves user in db

        refresh = RefreshToken.for_user(user)
        return Response({'user':UserSerializer(user).data,
                             'refresh':str(refresh),
                             'access':str(refresh.access_token),
                             'message':'User Created Successfully!'
                             }, status=status.HTTP_201_CREATED)

class CustomTokenObtainPairView(TokenObtainPairView):   #default jwt login view
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    #/api/users/me

class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

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
