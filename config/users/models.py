from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models


class User(AbstractUser):
    height = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True,help_text="height in cm")
    weight = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True,help_text="weight in kg")
    birth_date = models.DateField(null=True,blank=True)
    fitness_level = models.CharField(max_length=20,choices=[
        ('BEGINNER','Beginner'),
        ('INTERMEDIATE','Intermediate'),
        ('ADVANCED','Advanced'),
        ],default='BEGINNER')



    def __str__(self):
        return self.username



