from workouts.domain.workout_rules import WorkoutDomainService
from workouts.models import Workout
from django.utils import timezone

class WorkoutService:

    @staticmethod
    def get_today_workout(user,repo):
        workout = repo.today_workout(user)
        return workout
    @staticmethod

    def get_stats(user,repo):
        stats = repo.stats_last_30_days(user)

        for key,value in stats.items(): #for never returning non values and only returns zeros
            if value is None:
                stats[key] = 0

        return stats

    @staticmethod
    def create_workout(user,repo,data):
        today = timezone.now().date()
        if repo.today_workout(user):
            raise ValueError('You already logged workout for today')

        workout = Workout(
            user=user,
            date=data['date'],
            duration=data['duration'],
            workout_type = data['workout_type'],
            notes = data.get('notes',''),
        )
        return repo.save(workout)