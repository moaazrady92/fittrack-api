from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Food(models.Model):
    MEAL_TYPE = [
        ('BRK', 'Breakfast'),
        ('LUN', 'Lunch'),
        ('DIN', 'Dinner'),
    ]

    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='food')
    name = models.CharField(max_length=200)
    meal_type = models.CharField(max_length=3, choices=MEAL_TYPE)
    calories = models.PositiveIntegerField()
    proteins = models.DecimalField(max_digits=6, decimal_places=2,help_text='Protein in grams')
    carbs = models.DecimalField(max_digits=6, decimal_places=2,help_text='Carbs in grams')
    fats = models.DecimalField(max_digits=6, decimal_places=2,help_text='Fats in grams')
    date =models.DateField()
    time = models.TimeField(null=True,blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date','-time']

    def __str__(self):
        return f"{self.name} - {self.get_meal_type_display()}"
