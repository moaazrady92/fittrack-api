from datetime import timezone
from goals import serializers
from goals.models import Goal


class GoalService:

    @staticmethod
    def create_goal(user,data,repo):
        start = data.get('start_date')
        end = data.get('end_date')

        if start and end and end <start:
            raise ValueError('End must be after start')

        goal = Goal(
            user=user,
            repo=repo,
            start_date=start,
            end_date=end,
            description=data.get('description'),
            title=data.get('title'),
            goal_type=data.get('goal_type'),
            unit=data.get('unit',''),
            target=data.get('target'),
            date=data.get('date'),
            is_public=data.get('is_public'),
        )
        return repo.save(goal)

    @staticmethod
    def update_goal(goal,data,repo):
        start = data.get('start_date',goal.start_date)
        end = data.get('end_date',goal.end_date)

        if start and end and end <start:
            raise ValueError('End must be after start')

        for field , value in data.items():
            setattr(goal, field, value)

        GoalService._auto_update_status(goal)

        return repo.save(goal)

    @staticmethod
    def update_progress(goal,amount,repo):
        if goal.target_value is None:
            raise ValueError('Goal has no target value')

        new_value = goal.current_value + amount
        if new_value < 0:
            raise ValueError('Target value cannot be negative')

        goal.current_value = min(new_value,goal.target_value)
        GoalService._auto_update_status(goal)

        return repo.save(goal)

    @staticmethod
    def _auto_update_status(goal):
        today = timezone.now().date()

        if goal.target_value and goal.current_value >= goal.target_value:
            goal.status = 'Completed'

        elif today > goal.end_date:
            goal.status = 'Failed'

        elif goal.current_value > 0:
            goal.status = 'In progress'

        else:
            goal.status = 'Not_started'