from django.urls import path , include
from rest_framework import routers
from .views import ExerciseViewSet , WorkoutViewSet

router = routers.DefaultRouter()
router.register('exercises', ExerciseViewSet, basename='exercises')
router.register('workouts', WorkoutViewSet,basename='workouts')
urlpatterns = [
    path('', include(router.urls)),
]