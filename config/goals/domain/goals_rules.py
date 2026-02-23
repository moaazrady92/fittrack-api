from datetime import date

from rest_framework.exceptions import ValidationError

from goals.models import Goal


class GoalDomain:
    @staticmethod
    def validate_dates(start,end):
        if start and end and end < start:
            raise ValidationError("Start date cannot be greater than end date")

    @staticmethod
    def calculated_progress(current,amount,target):
        new_progress = current + amount
        if new_progress < target:
            return new_progress
        return new_progress

    @staticmethod
    def get_status(progress,target):
        if progress >= target:
            return "Completed"
        elif progress > 0:
            return "In progress"

        return "pending"

    @staticmethod
    def is_active(start,end):
        today = date.today()
        if start and today < start: # read it as if start exists and today is less that start then it returns false
            return False
        if end and today > end: # read it as if end exists and today is less that end then it returns false
            return False
        return True