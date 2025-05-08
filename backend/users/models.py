from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('HR', 'HR'),
        ('MANAGER', 'Manager'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='HR')