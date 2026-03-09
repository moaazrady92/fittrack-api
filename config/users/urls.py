from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.api.views import MyProfileView, ProfileDetailView, CoachDashboardView, TraineeDashboardView
from users.api.views import (
    RegisterView,
    CustomTokenObtainPairView,
    LogoutView,
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('profile/me/',MyProfileView.as_view(),name='my-profile'),
    path('profile/<str:username>',ProfileDetailView.as_view(),name='profile-details'),


    path('dashboard/coach', CoachDashboardView.as_view(), name='coach-dashboard'),
    path('dashboard/trainee', TraineeDashboardView.as_view(), name='trainee-dashboard')
]
