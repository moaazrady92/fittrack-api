from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
# swagger settings
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Fittrack API",
        default_version='v1.1',
        description="Fitness tracking Rest API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@fittrack.local"),
        license=openapi.License(name='MIT License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Swagger/OpenAPI documentation URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),

    # admin page
    path('admin/', admin.site.urls),

    # DRF authentication URLs (for browsable API)
    path('api-auth/', include('rest_framework.urls')),
    path('api/workouts/', include('workouts.urls')),
    path('api/', include('users.urls')),
    path('api/nutrition/', include('nutrition.urls')),
    path('api/leaderboard/', include('leaderboard.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/',TokenVerifyView.as_view(), name='token_verify'),
]


