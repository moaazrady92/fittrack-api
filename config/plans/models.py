from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

class Plan(models.Model):
    DIFFICULTY_CHOICES = [
        ('BEGINNER', 'beginner'),
        ('INTERMEDIATE', 'intermediate'),
        ('ADVANCED', 'advanced'),
    ]

    PLAN_TYPE = [
        ('WEIGHT_LOSS', 'weight_loss'),
        ('MUSCLE_GAIN', 'muscle_gain'),
        ('ENDURANCE', 'endurance'),
        ('GENERAL', 'general'),
    ]

    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_plans',
        limit_choices_to={'role': 'COACH','is_verified_coach': True},
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE, default='GENERAL')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    duration_weeks = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(52)])
    price = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)])
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_product_id = models.CharField(max_length=100, blank=True, null=True)

    subscriber_count = models.IntegerField(default=0)
    average_rating =  models.FloatField(default=0.0,validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_reviews = models.IntegerField(default=0)


    weekly_workouts = models.JSONField(default=dict, help_text='JSON structure for weekly workouts')

    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['coach','is_active']),
            models.Index(fields=['plan_type','difficulty']),
        ]

    def __str__(self):
        return f'{self.title} - {self.coach.username}'

    def update_rating(self,new_rating):
        total = self.average_rating * self.total_reviews + new_rating
        self.total_reviews += 1
        self.average_rating = total /self.total_reviews
        self.save()


class PlanSubscription(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'active'),
        ('CANCELED', 'canceled'),
        ('EXPIRED', 'expired'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE,related_name='subscriptions')
    stripe_subscription_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    cancelled_date = models.DateField(null=True, blank=True)
    auto_renew = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user','plan','status']

    def __str__(self):
        return f'{self.user.username} - {self.plan.title}'
