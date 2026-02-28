from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Food
from .serializers import FoodSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class FoodViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    serializer_class = FoodSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['meal_type', 'date']
    search_fields = ['name', 'notes']  # Search in food name or notes
    ordering_fields = ['date', 'time', 'calories']

    def get_queryset(self):
        return Food.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def today(self, request):
        today = timezone.now().date()
        today_foods = self.get_queryset().filter(date=today)

        if today_foods.exists():
            serializer = self.get_serializer(today_foods, many=True)
            return Response(serializer.data)
        return Response({'detail': 'No food entries logged for today'})

    @action(detail=False, methods=['get'])
    def daily_summary(self, request):
        date_str = request.query_params.get('date')
        if date_str:
            from datetime import datetime
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD'},
                                status=400)
        else:
            target_date = timezone.now().date()

        # Get food entries for the date
        daily_foods = self.get_queryset().filter(date=target_date)

        if not daily_foods.exists():
            return Response({
                'date': target_date,
                'detail': 'No food entries for this date',
                'summary': {
                    'total_calories': 0,
                    'total_protein': 0,
                    'total_carbs': 0,
                    'total_fats': 0,
                    'meal_count': 0
                }
            })

        # Calculate totals
        summary = daily_foods.aggregate(
            total_calories=Sum('calories'),
            total_protein=Sum('proteins'),
            total_carbs=Sum('carbs'),
            total_fats=Sum('fats'),
            meal_count=Count('id')
        )

        # Get meal breakdown
        meal_breakdown = {}
        for meal_code, meal_name in Food.MEAL_TYPE:
            meal_foods = daily_foods.filter(meal_type=meal_code)
            if meal_foods.exists():
                meal_summary = meal_foods.aggregate(
                    calories=Sum('calories'),
                    protein=Sum('proteins'),
                    carbs=Sum('carbs'),
                    fats=Sum('fats'),
                    count=Count('id')
                )
                meal_breakdown[meal_name] = meal_summary
                #now it became a list like {breakfast : calories... , proteins..... )

        return Response({
            'date': target_date,
            'summary': summary,
            'meal_breakdown': meal_breakdown,
            'foods': FoodSerializer(daily_foods, many=True).data
        })

    @action(detail=False, methods=['get'])
    def weekly_stats(self, request):
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)

        weekly_foods = self.get_queryset().filter(date__gte=week_ago,date__lte=today)
        weekly_totals = weekly_foods.aggregate(
            total_calories=Sum('calories'),
            avg_daily_calories=Avg('calories'),
            total_protein=Sum('proteins'),
            total_carbs=Sum('carbs'),
            total_fats=Sum('fats'),
            total_meals=Count('id'),
            avg_meals_per_day=Count('id') / 7.0  # Average per day
        )

        daily_breakdown = []
        for i in range(7):
            day = today - timedelta(days=i)
            day_foods = weekly_foods.filter(date=day)
            if day_foods.exists():
                day_summary = day_foods.aggregate(
                    calories=Sum('calories'),
                    protein=Sum('proteins'),
                    carbs=Sum('carbs'),
                    fats=Sum('fats'),
                    meals=Count('id')
                )
            else:
                day_summary = {
                    'calories': 0,
                    'protein': 0,
                    'carbs': 0,
                    'fats': 0,
                    'meals': 0
                }

            daily_breakdown.append({
                'date': day,
                'day_of_week': day.strftime('%A'),
                'summary': day_summary
            })

        # Meal type distribution
        meal_distribution = {}
        for meal_code, meal_name in Food.MEAL_TYPE:
            count = weekly_foods.filter(meal_type=meal_code).count()
            if count > 0:
                meal_distribution[meal_name] = count

        return Response({
            'period': {
                'start': week_ago,
                'end': today,
                'days': 7
            },
            'weekly_totals': weekly_totals,
            'daily_breakdown': daily_breakdown,
            'meal_distribution': meal_distribution
        })

    @action(detail=False, methods=['get'])
    def calorie_goal(self, request):
        date_str = request.query_params.get('date')
        if date_str:
            from datetime import datetime
            try:
                target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid date format'}, status=400)
        else:
            target_date = timezone.now().date()

        queryset =  self.get_queryset().filter(date=target_date)
        total_calories = queryset.aggregate(total=Sum('calories'))['total'] or 0
        daily_goal = request.user.daily_calorie_goal

        progress_percentage = min((total_calories / daily_goal) * 100, 100) if daily_goal > 0 else 0
        remaining_calories = max(daily_goal - total_calories, 0)

        return Response({
            'date': target_date,
            'daily_goal': daily_goal,
            'consumed': total_calories,
            'remaining': remaining_calories,
            'progress_percentage': round(progress_percentage, 1),
            'status': 'under' if total_calories < daily_goal else 'over' if total_calories > daily_goal else 'met'
        })

    @action(detail=False, methods=['get'])
    def search_food(self, request):
        search_query = request.query_params.get('q', '')
        if not search_query:
            return Response({'error': 'Please provide a search query (?q=...)'},
                            status=400)

        # Search in food names and notes
        results = self.get_queryset().filter(
            Q(name__icontains=search_query) |
            Q(notes__icontains=search_query)
        )[:20]  # Limit to 20 results

        serializer = self.get_serializer(results, many=True)
        return Response({
            'query': search_query,
            'count': results.count(),
            'results': serializer.data
        })