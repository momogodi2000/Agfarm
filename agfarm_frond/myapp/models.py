from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("financial_institution", "Financial Institution"),
        ("farmer", "Farmer"),
        ('buyer', 'Buyer'),
        ("government_agency", "Government Agency"),
        ("logistics_provider", "Logistics Provider"),
    ]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=12, unique=True, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
