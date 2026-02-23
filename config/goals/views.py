from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .repositories.goals_repository import GoalRepository
from .services.goals_services import GoalService
from .serializers import GoalsSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, permissions, filters , serializers

class GoalsViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = GoalsSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['goal_type', 'status','date']
    search_fields = ['goal_type', 'status_choice']  # Search in food name or notes

    def get_queryset(self):
        return GoalRepository.get_by_user(self.request.user)

    def perform_create(self, serializer):
        try:
            goal = GoalService.create_goal(
                user=self.request.user,
                data=serializer.validated_data,
                repo=GoalRepository,
            )
            serializer.instance = goal
        except Exception as e:
            raise serializers.ValidationError({'detail': str(e)})

    def perform_update(self, serializer):
        try:
            goal = GoalService.update_goal(
                user=self.request.user,
                goal=self.get_object(),
                data=serializer.validated_data,
                repo=GoalRepository,
            )
            serializer.instance = goal
        except Exception as e:
            raise serializers.ValidationError({'detail': str(e)})

    def perform_destroy(self, instance):
        GoalService.delete_goal(
            user=self.request.user,
            goal=instance,
            repo=GoalRepository,
        )

    @action(detail=False, methods=['get'])
    def active(self, request):
        goals = GoalService.get_active_goals(
            user=self.request.user,
            repo=GoalRepository,
        )
        serializer = self.get_serializer(goals, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def update_progress(self, request,pk=None):
        goal = self.get_object()
        value = request.data.get('value')

        if value is None:
            return Response({
                'detail':'value is required'
            },status=status.HTTP_400_BAD_REQUEST)

        try:
            updated_goal = GoalService.update_goal(
                goal=goal,
                user=self.request.user,
                value=value,
                repo=GoalRepository,
            )
            serializer = self.get_serializer(updated_goal)
            return Response(serializer.data)
        except Exception as e:
            raise serializers.ValidationError({'detail': str(e)},status=status.HTTP_400_BAD_REQUEST)
