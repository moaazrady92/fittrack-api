from goals.models import Goal
from django.utils import timezone
from django.db.models import Q

class GoalRepository:

    @staticmethod
    def get_user_goals(user):
        return Goal.objects.filter(user=user)

    @staticmethod
    def get_by_id(user,goal_id):
        return Goal.objects.filter(pk=goal_id, user=user).first()

    @staticmethod
    def save(goal):
        goal.save()
        return goal

    @staticmethod
    def delete(goal):
        goal.delete()
        return goal

    @staticmethod
    def get_active_goals(user):
        today = timezone.now().date()
        return Goal.objects.filter(user=user).filter(
        Q(start_date__lte=today) | Q(end_date__isnull=True),
              Q(end_date__gte=today) | Q(start_date__isnull=True),
        )

    @staticmethod
    def get_completed_goals(user):
        return Goal.objects.filter(user=user,status='COMPLETED')
