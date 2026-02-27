from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Workout, Exercise
from .repositories.workout_repository import WorkoutRepository
from .serializers import ExerciseSerializer, WorkoutSerializer
from django.db import models
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication
from .services.workout_services import WorkoutService

class WorkoutViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['workout_type', 'date']
    search_fields = ['notes']
    ordering_fields = ['-date', 'duration']

    def get_queryset(self):
        return WorkoutRepository.get_user_workout(self.request.user)

    def perform_create(self, serializer):
        try:
            workout = WorkoutService.create_workout(
                user = self.request.user,
                data = serializer.validated_data,
                repo = WorkoutRepository
            )
            serializer.instance = workout

        except ValueError as e:
            raise serializers.ValidationError({'detail': str(e)})


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
        workout = WorkoutService.get_today_workout(
            user=request.user,
            repo = WorkoutRepository
        )

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
        stats = WorkoutService.get_stats(
            user=request.user,
            repo = WorkoutRepository
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