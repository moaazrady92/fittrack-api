class WorkoutDomainService:

    @staticmethod
    def validate_duration(duration : int):
        if duration < 1:
            raise ValueError("duration must be greater than 1 minute")
        elif duration > 240:
            raise ValueError("duration must be less than 240 minutes")

    @staticmethod
    def validate_unique_workout(user,date,workout_repo):
        if workout_repo.exists_for_user_on_date(user,date):
            raise ValueError("You already logged a workout for this date")
