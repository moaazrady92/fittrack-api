from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Goal(models.Model):
    GOAL_TYPES = [
        ('WEIGHT', 'Weight Loss/Gain'),
        ('STRENGTH', 'Strength'),
        ('ENDURATION', 'Endurance'),
        ('NUTRITION', 'Nutrition'),
        ('GENERAL', 'General Fitness'),
    ]

    STATUS_CHOICES = [
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    user = models.ForeignKey('user.User', on_delete=models.CASCADE,related_name='goals')
    title = models.CharField(max_length=200)
    goal_type = models.CharField(max_length=200, choices=GOAL_TYPES)
    description = models.TextField(blank=True)
    target_value = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    current_value = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    unit = models.CharField(max_length=50, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='NOT_STARTED')
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-end_date']

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

    def progress_percentage(self):
        if self.target_value:
            return (self.current_value / self.target_value) * 100
        return 0

    def days_remaining(self):
        from django.utils import timezone
        from datetime import date
        today = date.today()
        return max(0,(self.end_date - today).days)