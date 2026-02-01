from django.shortcuts import render
from rest_framework import viewsets , permissions , filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Workout , Exercise
from .serializers import ExerciseSerializer , WorkoutSerializer
from django.db import models
from rest_framework import serializers


class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['workout_type','date'] # so you can search workout types and their date
    search_fields = ['notes'] # so you can search for a specific word in the notes
    ordering_fields = ['-date','duration'] # -date --> newest first , date --> oldest first , duration --> shortest first , -duration --> longest first

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def today(self,request):
        from django.utils import timezone
        today = timezone.now().date()
        workout = self.get_queryset().filter(date=today).first()

        if workout:
            serializer = self.get_serializer(workout)
            return Response(serializer.data)
        return Response({'detail':'No workout logged for today'})

    @action(detail=False, methods=['get'])
    def stats(self,request):
        from django.db.models import Count ,Sum , Avg
        from django.utils import timezone
        from datetime import timedelta

        last_30_days = timezone.now().date() - timedelta(days=30)

        stats = self.get_queryset().filter(date__gte=last_30_days).aggregate(
            total_workout = Count('id'),
            total_duration = Sum('duration'),
            avg_duration = Avg('duration'),
            strength_count = Count('id', filter=models.Q(workout_type='STR')),
            cardio_count = Count('id', filter=models.Q(workout_type='CAR')),
            )
        return Response(stats)

class ExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Exercise.objects.filter(workout__user=self.request.user)

    def perform_create(self, serializer):
        workout = serializer.validated_data.get('workout')
        if workout.user != self.request.user:
            raise serializers.ValidationError('You can only add exercises to your own workouts')
        serializer.save()
