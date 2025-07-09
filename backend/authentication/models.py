from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('store_owner', 'Store Owner'),
        ('admin', 'Admin'),
    )

    email = models.EmailField(unique=True)
    user_Type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.email} ({self.user_Type})'