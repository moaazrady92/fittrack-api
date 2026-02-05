from rest_framework import serializers
from .models import Food

class FoodSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Food
        fields = [
            'id', 'user', 'user_id','name','meal_type',
            'calories','proteins','carbs','fats',
            'date','time','notes','get_meal_type_display'
        ]
        read_only_fields = ['id', 'user', 'user_id']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['meal_type_display'] = instance.get_meal_type_display()
        return representation