
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('EVENT_PLANNER', 'Event Planner'),
        ('VENDOR', 'Vendor'),
        ('CLIENT', 'Client'),
    )
    otp = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ADMIN')

    def __str__(self):
        return self.username