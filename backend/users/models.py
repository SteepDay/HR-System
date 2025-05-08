from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLES = (
        ('HR', 'HR'),
        ('MANAGER', 'Manager'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='HR')
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()  # Используем наш кастомный менеджер

    def __str__(self):
        return self.email