from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'role'
        ]
        read_only_fields = ['role']

class UserForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class UpdateUserForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=255)
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    
    def validate(self, attrs):
        if attrs.get('password')!= attrs.get('confirm_password'):
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match'
            })
        return super().validate(attrs)
    
    def update(self, user, validated_data):
        otp = validated_data.get('otp')
        email = validated_data.get('email')
        
        if otp == user.otp and email == user.email:
            user.password = make_password(validated_data.get('password'))
            
            user.save()
        else:
            raise serializers.ValidationError({
                'otp': 'Invalid OTP.'
            })
            
        return user