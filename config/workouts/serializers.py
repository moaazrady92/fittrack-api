from rest_framework import serializers
from .models import Workout ,Exercise


class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = ['id','name','sets','reps','weight','rest_time','order']
        read_only_fields = ['id']

class WorkoutSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True) #this shows username not id
    user_id = serializers.PrimaryKeyRelatedField(read_only=True) #shows the actual id number

    class Meta:
        model = Workout
        fields = ['id','user','user_id','date','duration','workout_type','notes',
                  'exercises','created_at']
        read_only_fields = ['id','user','user_id','created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_duration(self,value):
        if value < 1:
            raise serializers.ValidationError('Workout duration must be greater than a minute')
        if value > 240:
            raise serializers.ValidationError('Workout duration must be less than 240 minutes')
        return value