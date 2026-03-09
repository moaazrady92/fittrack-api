from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken #for generating and blacklist tokens and refresh token lives long unlike access token
from rest_framework.parsers import MultiPartParser , FormParser
from rest_framework.generics import (
    GenericAPIView,
    RetrieveUpdateAPIView ,
    CreateAPIView
)


import logging
from users.services.email_service import EmailService
from plans.models import Plan
from .serializers import CoachProfileSerializer, TraineeProfileSerializer, BaseProfileSerializer
from .serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
    RegisterSerializer
)
from ..services.user_service import DashboardService

logger = logging.getLogger(__name__)
User = get_user_model()

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) #requisting data from serializers first
        serializer.is_valid(raise_exception=True)
        user = serializer.save() #saves user in db
        self.send_welcome_email(user)

        refresh = RefreshToken.for_user(user)
        return Response({
            'user':UserSerializer(user).data,
            'refresh':str(refresh),
            'access':str(refresh.access_token),
            'message':'Registration Successful! Check your email for welcome message. '
                }, status=status.HTTP_201_CREATED)

    def send_welcome_email(self,user):
        try :
            EmailService.send_welcome_email(user)
        except Exception as e:
            logger.error(f"Failed to send welcome email :{str(e)}")

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
        except Exception:
            return Response({
                'error':'invalid token'
            },status =status.HTTP_400_BAD_REQUEST
            )

class ProfileDetailView(generics.RetrieveAPIView):
    queryset = Plan.objects.filter(is_public=True)
    serializer_class = BaseProfileSerializer
    lookup_field = 'username'
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        user = self.get_object()
        return CoachProfileSerializer if user.role.is_coach() else TraineeProfileSerializer

class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = BaseProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser,FormParser]  #multipartparser for when you use an image since it cant be in json form you just multipart-parser

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        return CoachProfileSerializer if self.request.user.role.is_coach() else TraineeProfileSerializer

    def update(self,request,*args,**kwargs):
        partial = kwargs.pop('partial',True) #accepts partial updates like bio for example
        instance = self.get_object() #returns self.user which updates the user info right away
        serializer = self.get_serializer(instance,data=request.data,partial=partial) #checks first if field exists then checks if the data type is correct then validates data
        serializer.is_valid(raise_exception=True) #if the data is correct
        self.perform_update(serializer) #updates it and saves to database

        return Response({
            'message' : 'Successfully updated your profile!',
            'profile' : serializer.data
        }) #returns a custom response

class CoachDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user

        if not user.role.is_coach():
            self.permission_denied(
                request,
                message='Only coaches can access this page'
            )
        coach_stats = DashboardService.get_coach_stats(user)

        return Response({
            'coach': user.username,
            'stats' : coach_stats
        })

class TraineeDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not user.role.is_trainee():
            self.permission_denied(
                request,
                message='Only Trainees can access this page'
            )
        trainee_stats = DashboardService.get_trainee_stats(user)

        return Response({
            'trainee':user.username,
            'stats' : trainee_stats
        })