from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Exercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name