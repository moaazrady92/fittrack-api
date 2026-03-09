from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from plans.models import PlanSubscription , Plan
from django.db.models import Avg


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'height', 'weight', 'birth_date', 'fitness_level',
            'is_public', 'date_joined', 'last_login'
                  ]
        read_only_fields = ['id','date_joined','last_login']

    def validate_email(self,value): # since we will login via email
        qs = User.objects.filter(email=value)

        if self.instance:
            qs = qs.exclude(id=self.instance.id)
            # the reason we use exclude your own email to avoid "your email already exists (your own email)" error

        if qs.exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return value

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod # for calling the class itself without needing to call it like class()
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['user_id'] = user.id
        return token

    def validate(self,attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        data['message'] = 'Login successful.'
        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = User
        fields = [
            'username','email','password','password2',
            'first_name','last_name',
            'height','weight','birth_date',
            'fitness_level','is_public',
                  ]

    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'Passwords Dont match'
            })
        return attrs

    def validate_email(self,value):
        qs = User.objects.filter(email=value)

        if self.instance:
            qs = qs.exclude(id=self.instance.id)

        if qs.exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return value

    def create(self,validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)

class BaseProfileSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id','username','email','first_name','last_name', 'full_name',
            'profile_picture', 'bio' , 'age','birth_date',
            'height','weight','fitness_level','is_public',
            'date_joined'
        ]
        read_only_fields = ['id','date_joined']

    def get_age(self,obj):
        return obj.age

    def get_full_name(self,obj):
        return obj.get_full_name()

class TraineeProfileSerializer(BaseProfileSerializer):

    class Meta(BaseProfileSerializer):
        fields = BaseProfileSerializer.Meta.fields + [
            'current_goal',
            'preferred_workout_days'
        ]

class CoachProfileSerializer(serializers.ModelSerializer):
    total_plans = serializers.SerializerMethodField()
    total_subscribers = serializers.SerializerMethodField()
    active_subscribers = serializers.SerializerMethodField()
    average_plan_rating = serializers.SerializerMethodField()

    class Meta(BaseProfileSerializer.Meta):
        fields = BaseProfileSerializer.Meta.fields + [
            'phone_number','is_verified_coach', 'coach_specialization',
            'years_experience','total_plans' , 'total_subscribers',
            'active_subscribers','average_plan_rating'
        ]

    def get_total_plans(self,obj):
        if hasattr(obj,'created_plans'):
            return obj.created_plans.count()
        return 0

    def get_total_subscribers(self,obj):
        return PlanSubscription.objects.filter(
            plan__coach=obj
        ).count()

    def get_active_subscribers(self,obj):
        return PlanSubscription.objects.filter(
            plan__coach=obj,
            status='ACTIVE'
        ).count()

    def get_average_plan_rating(self,obj):
        avg = Plan.objects.filter(
            coach=obj,
            average_rating__gte=0
        ).aggregate(Avg('average_rating'))['average_rating__avg']

        return round(avg,1) if avg else 0
