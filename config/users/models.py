from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    ROLE_CHOICE = [
        ('COACH','Coach'),
        ('TRAINEE','trainee'),
    ]

    FITNESS_LEVEL = [
        ('BEGINNER','Beginner'),
        ('INTERMEDIATE','Intermediate'),
        ('ADVANCED','Advanced'),
    ]

    email = models.EmailField('email address', unique=True) # for ensuring uniqueness of email
    height = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True,help_text="height in cm")
    weight = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True,help_text="weight in kg")
    birth_date = models.DateField(null=True,blank=True)
    fitness_level = models.CharField(max_length=20,choices=FITNESS_LEVEL,default='BEGINNER')
    profile_picture = models.ImageField(upload_to='profile_pictures/',null=True,blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICE, default='TRAINEE')
    is_public = models.BooleanField(default=False)
    is_verified_coach = models.BooleanField(default=False)

    stripe_customer_id = models.CharField(max_length=20,null=True,blank=True)

    coach_bio = models.TextField(blank=True)
    coach_specialization = models.CharField(max_length=20,null=True,blank=True)
    years_experience = models.IntegerField(default=0)


    class Meta:
        db_table = 'users'
        ordering = ['date_joined']

    def __str__(self):
        return f'{self.username} ({self.role})'

    # these are called helper functions so instead of everytime you need to make sure that user is coach you just write request.user.is_coach() instead
    def is_coach(self):
        return self.role == 'COACH'

    def is_trainee(self):
        return self.role == 'TRAINEE'

    def age(self):
        if self.birth_date:
            from datetime import date
            today = date.today()
            return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None

    def get_full_name(self,):
        return f'{self.first_name} {self.last_name}'.strip() or None






