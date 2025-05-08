from django.db import models
from users.models import User

class Vacancy(models.Model):
    STATUS_CHOICES = [
        ('OPEN', 'Открыта'),
        ('CLOSED', 'Закрыта'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='OPEN')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vacancies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title