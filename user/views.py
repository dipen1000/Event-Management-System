from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from random import randint
from django.conf import settings

from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import *
from .serializers import *
from .permissions import *

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'role': user.role
        })

class UserProfileListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [
        IsAuthenticated, IsAdminUser
    ] 

    def get(self, request, *args, **kwargs):
        '''print(request.user.role) '''
        return super().get(request, *args, **kwargs)
    
class UserProfileDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]  

    def get_object(self):
        return self.request.user
    
class UserView(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    #? This view is for Update Forgot Password 
    @swagger_auto_schema(
        methods=['post'],
        request_body=UserForgotPasswordSerializer
    )
    @action(methods=['post'],detail=False)
    def send_otp_forgot_password(self, request):
        user = get_object_or_404(User, email=request.data.get('email'))
        serializer = UserForgotPasswordSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user.otp = str(randint(0000,9999))
        user.save()
        
        send_mail(
            subject='Forgot Password OTP',
            message=f'Your otp is {user.otp} for {user.email}',
            from_email=settings.SENDER_EMAIL_USER,
            recipient_list=[
                user.email
            ]
        )
        return Response({
            'details':f'OTP has been successfully sent to {user.email}.'
        })
        
    #? This view is for Update Forgot Password 
    @swagger_auto_schema(
        methods=['put'],
        request_body=UpdateUserForgotPasswordSerializer
    )
    @action(methods=['put'],detail=False)
    def update_forgot_password(self, request):
        user = get_object_or_404(User, email=request.data.get('email'))
        serializer = UpdateUserForgotPasswordSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'details':f'Password has been successfully updated for {user.email}'
        })
        
        
    