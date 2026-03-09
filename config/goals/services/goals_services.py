from django.utils import timezone
from goals.models import Goal
from goals.domain.goals_rules import GoalDomain


class GoalService:

    @staticmethod
    def create_goal(user, data, repo):
        start = data.get("start_date")
        end = data.get("end_date")

        GoalDomain.validate_dates(start, end)

        goal = Goal(
            user=user,
            start_date=start,
            end_date=end,
            description=data.get("description"),
            title=data.get("title"),
            goal_type=data.get("goal_type"),
            unit=data.get("unit", ""),
            target=data.get("target"),
            date=data.get("date"),
            is_public=data.get("is_public"),
        )

        return repo.save(goal)

    @staticmethod
    def update_goal(goal, data, repo):
        start = data.get("start_date", goal.start_date)
        end = data.get("end_date", goal.end_date)

        GoalDomain.validate_dates(start, end)

        for field, value in data.items():
            setattr(goal, field, value)

        GoalService._auto_update_status(goal)

        return repo.save(goal)

    @staticmethod
    def update_progress(goal, amount, repo):

        if goal.target is None:
            raise ValueError("Goal has no target")

        new_progress = goal.progress + amount

        if new_progress < 0:
            raise ValueError("Progress cannot be negative")

        goal.progress = min(new_progress, goal.target)

        GoalService._auto_update_status(goal)

        return repo.save(goal)

    @staticmethod
    def delete_goal(user, goal, repo):
        if goal.user != user:
            raise ValueError("Unauthorized")

        repo.delete(goal)

    @staticmethod
    def _auto_update_status(goal):
        today = timezone.now().date()

        if goal.target and goal.progress >= goal.target:
            goal.status = "Completed"

        elif goal.end_date and today > goal.end_date:
            goal.status = "Failed"

        elif goal.progress > 0:
            goal.status = "In progress"

        else:
            goal.status = "Not_started"