from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'height', 'weight', 'birth_date', 'fitness_level',
                  'is_public', 'date_joined', 'last_login')

        read_only_fields = ['id','date_joined','last_login','is_staff','is_active','is_superuser']

    def validate_email(self,value):
        if User.objects.filter(email=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return value

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
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
        fields = ['username','email','password','password2',
                 'first_name','last_name',
                 'height','weight','birth_date',
                  'fitness_level','is_public',
                  ]

    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'Password':'Passwords dont match.'
                                               })
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("A user with this email already exists.")

        return attrs

    def create(self,validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


