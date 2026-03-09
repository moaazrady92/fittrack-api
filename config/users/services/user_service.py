from plans.models import Plan, PlanSubscription
from django.db.models import Count


class DashboardService:

    @staticmethod
    def get_coach_stats(user):
        return Plan.objects.filter(coach=user).aggregate(
            plans_created=Count('id'),
            total_subscribers =Count('subscribers'),
        )

    @staticmethod
    def get_trainee_stats(user):
        active_subscribers = PlanSubscription.objects.filter(
            user=user,
            status='ACTIVE'
        ).count()

        return {
            'active_subscribers': active_subscribers,
            'nutrition_streak' : 0
        }