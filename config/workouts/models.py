from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings

class Workout(models.Model):
    WORKOUT_TYPES = [
        ('STR', 'strength'),
        ('CAR','cardio'),
        ('HIIT','HIIT'),
        ('FLEX','flexibility'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workouts')
    date = models.DateField()
    duration = models.PositiveIntegerField(help_text='duration in minutes', validators=[MinValueValidator(1)])
    workout_type = models.CharField(max_length=4, choices=WORKOUT_TYPES, default='STR')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.date} - {self.get_workout_type_display()}"

class Exercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE,related_name='exercises')
    name = models.CharField(max_length=100)
    sets = models.PositiveIntegerField(default=3)
    reps = models.PositiveIntegerField(default=10)
    weight = models.DecimalField(max_digits=6, decimal_places=2,help_text='weight in kg')
    rest_time = models.PositiveIntegerField(default=60,help_text='time in seconds')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.sets}x{self.reps} at {self.weight} kg"
