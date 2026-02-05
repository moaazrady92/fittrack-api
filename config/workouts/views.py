from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Workout, Exercise
from .serializers import ExerciseSerializer, WorkoutSerializer
from django.db import models
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['workout_type', 'date']
    search_fields = ['notes']
    ordering_fields = ['-date', 'duration']

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Retrieve a list of workouts with optional filtering",
        manual_parameters=[
            openapi.Parameter(
                'workout_type',
                openapi.IN_QUERY,
                description="Filter by workout type",
                type=openapi.TYPE_STRING,
                enum=['STR', 'CAR', 'HIIT', 'FLEX']
            ),
            openapi.Parameter(
                'date',
                openapi.IN_QUERY,
                description="Filter by specific date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search in workout notes",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: WorkoutSerializer(many=True),
            401: 'Unauthorized',
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Get today's workout entry",
        responses={
            200: WorkoutSerializer,
            404: openapi.Response(
                description="No workout found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    @action(detail=False, methods=['get'])
    def today(self, request):
        from django.utils import timezone
        today = timezone.now().date()
        workout = self.get_queryset().filter(date=today).first()

        if workout:
            serializer = self.get_serializer(workout)
            return Response(serializer.data)
        return Response({'detail': 'No workout logged for today'})

    @swagger_auto_schema(
        operation_description="Get workout statistics for the last 30 days",
        responses={
            200: openapi.Response(
                description="Workout statistics data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_workout': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Total number of workouts"
                        ),
                        'total_duration': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Total duration in minutes"
                        ),
                        'avg_duration': openapi.Schema(
                            type=openapi.TYPE_NUMBER,
                            format='float',
                            description="Average duration in minutes"
                        ),
                        'strength_count': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Number of strength workouts"
                        ),
                        'cardio_count': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            description="Number of cardio workouts"
                        ),
                    }
                ),
                examples={
                    'application/json': {
                        'total_workout': 12,
                        'total_duration': 720,
                        'avg_duration': 60.0,
                        'strength_count': 8,
                        'cardio_count': 4
                    }
                }
            )
        }
    )
    @action(detail=False, methods=['get'])
    def stats(self, request):
        from django.db.models import Count, Sum, Avg
        from django.utils import timezone
        from datetime import timedelta

        last_30_days = timezone.now().date() - timedelta(days=30)

        stats = self.get_queryset().filter(date__gte=last_30_days).aggregate(
            total_workout=Count('id'),
            total_duration=Sum('duration'),
            avg_duration=Avg('duration'),
            strength_count=Count('id', filter=models.Q(workout_type='STR')),
            cardio_count=Count('id', filter=models.Q(workout_type='CAR')),
        )

        # Handle None values
        for key, value in stats.items():
            if value is None:
                stats[key] = 0

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