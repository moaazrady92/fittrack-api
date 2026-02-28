from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from nutrition.repository.food_repository import FoodRepository

class FoodService:

    @staticmethod
    def get_today_food(user):
        today = timezone.now().date()
        return FoodRepository.food_by_date(user,today)

    @staticmethod
    def get_daily_summary(user,date):
        food = FoodRepository.food_by_date(user,date)

        if not food.exists():
            return {
                'summary': {
                    'total_calories' : 0 ,
                    'total_protein' : 0 ,
                    'total_fats' : 0 ,
                    'total_carbs' : 0 ,
                    'meal_count' : 0 ,
                 },
                'meal_breakdown' : {}, #dict because it's represented like {'Breakfast' : ... , lunch : ....}
                'food' : [] # list because it returns multiple entries like [ {'name' : 'eggs', ....} , ....]
            }

        summary = FoodRepository.aggregate_total(food)

        meal_breakdown = {}
        for code , name in food.model.MEAL_TYPE:
            meal_food = food.filter(meal_type=code)
            if meal_food.exists():
                meal_breakdown[code] = FoodRepository.aggregate_total(meal_food)

        return {
            'summary' : summary,
            'meal_breakdown' : meal_breakdown,
            'food' : food
        }

    @staticmethod
    def get_weekly_stats(user):
        weekly_food = FoodRepository.weekly_food(user)
        distribution = FoodRepository.meal_distribution(weekly_food)

        return weekly_food, distribution

    @staticmethod
    def calorie_goal_progress(user,date):
        food = FoodRepository.food_by_date(user,date)

        total_calories = food.aggregate(total=sum([f.calories for f in food]))['total'] or 0
        daily_goal = user.daily_calorie_goal

        progress = min((total_calories / daily_goal) * 100, 100) if daily_goal > 0 else 0
        remaining = max((daily_goal - total_calories), 0)

        return {
            'daily_goal' : daily_goal,
            'remaining' : remaining,
            'total_calories' : total_calories,
            'progress_percentage' : round(progress,1),
            'status' : (
                'under' if total_calories < daily_goal
                else 'over' if total_calories > daily_goal
                else 'met'
            )
        }