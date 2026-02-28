from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Food
from .serializers import FoodSerializer
from services.food_service import FoodService
from rest_framework_simplejwt.authentication import JWTAuthentication


class FoodViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['meal_type', 'date']
    search_fields = ['name', 'notes']
    ordering_fields = ['date', 'time', 'calories']

    def get_queryset(self):
        return Food.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def today(self, request):
        today = timezone.now().date()
        data = FoodService.get_food_by_date(request.user, today)
        return Response(data)

    @action(detail=False, methods=['get'])
    def daily_summary(self, request):
        date = FoodService.parse_date(request)
        data = FoodService.get_daily_summary(request.user, date)
        return Response({'date': date, **data})

    @action(detail=False, methods=['get'])
    def weekly_stats(self, request):
        data = FoodService.get_weekly_stats(request.user)
        return Response(data)

    @action(detail=False, methods=['get'])
    def calorie_goal(self, request):
        date = FoodService.parse_date(request)
        data = FoodService.calorie_goal_progress(request.user, date)
        return Response({'date': date, **data})

    @action(detail=False, methods=['get'])
    def search_food(self, request):
        query = request.query_params.get('q', '').strip() #strip for removing spaces
        #example : get /search_food/?q=chicken
        if not query:
            return Response(
                {'error': 'Please provide a search query (?q=...)'},
                status=400
            )

        data = FoodService.search_food(request.user, query)
        return Response(data)