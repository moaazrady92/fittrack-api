from rest_framework import serializers

from plans.models import Plan


class PlanSerializer(serializers.ModelSerializer):
    coach_name = serializers.CharField(source='coach.username',read_only=True)
    subscriber_count = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = [
            'id','title','description','plan_type', 'difficulty',
            'duration_weeks','price','coach','coach_name',
            'subscriber_count','is_active','is_featured'
        ]
        read_only_fields = ['id','coach','coach_name','subscriber_count']

    def get_subscriber_count(self,obj):
        return obj.subcription.filter(status='ACTIVE').count()

class PlanDetailSerializer(serializers.ModelSerializer):
    coach_name = serializers.CharField(source='coach.username',read_only=True)
    weekly_workouts = serializers.JSONField()
    subscriber_count = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Plan
        fields = [
            'id','title','description','plan_type', 'difficulty',
            'duration_weeks','price','stripe_price_id','stripe_product_id',
            'coach','coach_name','subscriber_count','average_rating',
            'weekly_workouts','is_active','is_featured','created_at','updated_at'
        ]
        read_only_fields = [
            'id','coach','coach_name','subscriber_count',
            'average_rating','created_at','updated_at'
        ]