from rest_framework import serializers
from .models import Goal

class GoalsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    goal_type_display = serializers.CharField(source='goal_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()


    class Meta:
        model = Goal
        fields = ['id','user','user_id',
                  'title','goal_type','goal_type_display',
                  'status','status_display','unit',
                  'progress_percentage','days_remaining','is_public',
                  'current_value','target_value','start_date',
                  'end_date','description'
                  ]

        read_only_fields = ['id','user',
                            'user_id','progress_percentage',
                            'goal_type_display','status_display',
                            'days_remaining'
                            ]

    def get_progress_percentage(self, obj):
        return round(obj.progress_percentage(),2)

    def get_days_remaining(self, obj):
        return obj.days_remaining()

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        start = data.get('start_date')
        end = data.get('end_date')

        if start and end and end < start:  # this ensures that both of them exist so it would compare the time
            raise serializers.ValidationError({'start_date':"The start date must be greater than the end date"})

        return data