from django.urls import path, include
from rest_framework.routers import DefaultRouter
from plans.api.views import PlanViewSet

router = DefaultRouter()
router.register('', PlanViewSet,basename='Plan')

urlpatterns = [
    path('', include(router.urls)),
]