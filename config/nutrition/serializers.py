from rest_framework import serializers
from .models import Food

class FoodSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    meal_type_display = serializers.CharField(source='get_meal_type_display',read_only=True)

    class Meta:
        model = Food
        fields = [
            'id', 'user', 'user_id','name','meal_type',
            'meal_type_display','calories','proteins','carbs','fats',
            'date','time','notes'
        ]
        read_only_fields = ['id', 'user', 'user_id','meal_type_display']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
