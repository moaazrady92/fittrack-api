from django.urls import path , include
from rest_framework import routers
from .views import ExerciseViewSet , WorkoutViewSet

router = routers.DefaultRouter()
router.register('exercises', ExerciseViewSet)
router.register('workouts', WorkoutViewSet)
urlpatterns = [
    path('', include(router.urls)),
]