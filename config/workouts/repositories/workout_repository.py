from workouts.models import Workout
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q , Sum , Avg , Count

class WorkoutRepository:

    @staticmethod
    def get_user_workout(user):
        return Workout.objects.filter(user=user)

    @staticmethod
    def save(workout):
        workout.save()
        return workout

    @staticmethod
    def user_workout(user):
        return Workout.objects.filter(user=user)

    @staticmethod
    def today_workout(user):
        today = timezone.now().date()
        return Workout.objects.filter(user=user, date=today).first()

    @staticmethod
    def stats_last_30_day(user):

        last_30_days = timezone.now().date() - timedelta(days=30)
        return Workout.objects.filter(
            user=user,
            date__gte=last_30_days
        ).aggregate(
            total_workout=Count('id'),
            total_duration=Sum('duration'),
            avg_duration=Avg('duration'),
            strength_count=Count('id', filter=Q(workout_type='STR')),
            cardio_count=Count('id', filter=Q(workout_type='CAR'))
        )


