from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from workouts.models import Workout


class LeaderboardRepository:

    @staticmethod
    def get_top_users_by_duration(days=30,limit=30):
        start_date = timezone.now() - timedelta(days=days)

        return (
            Workout.objects
            .filter(date__gte=start_date)
            .values('user')
            .annotate(total_duration=Sum('duration'))
            .order_by('-total_duration')[:limit]
        )