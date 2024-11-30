from django.urls import path, include
from .views import *

from rest_framework import routers
router = routers.SimpleRouter()

router.register('user',UserView, basename='user')

urlpatterns = [
    # path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('profiles/', UserProfileListView.as_view(), name='profiles'),
    path('profiles/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/me/', UserProfileDetailView.as_view(), name='my-profile'),
    path('', include(router.urls))
]