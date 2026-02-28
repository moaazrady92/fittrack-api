from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone
from nutrition.models import Food

class FoodRepository:

    @staticmethod
    def get_user_foods(user):
        return Food.objects.filter(user=user)

    @staticmethod
    def get_user_food_date(user,date):
        return Food.objects.filter(user=user,date=date)

    @staticmethod
    def weekly_food(user,date):
        today = timezone.now().date()
        week_ago = timezone.now() - timedelta(days=7)
        return Food.objects.filter(user=user,date__lte=today,week_ago__gte=week_ago)

    @staticmethod
    def aggregate_total(queryset):
        return queryset.aggregate(
            total_calories=Sum('calories'),
            total_protein=Sum('protein'),
            total_carbs=Sum('carbs'),
            total_fats=Sum('fats'),
            meal_count=Sum('id'),
        )

    @staticmethod
    def meal_distribution(queryset):
        distribution = {}

        for code , name in Food.MEAL_TYPE:
            count = queryset.filter(meal_type=code).count()
            if count > 0:
                distribution[name] = count

            #it becomes like Breakfast : 1 , Lunch : 2 , Dinner : 10

        return distribution
