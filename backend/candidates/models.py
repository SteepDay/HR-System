from django.db import models
from users.models import User
from vacancies.models import Vacancy

class Candidate(models.Model):
    class Status(models.TextChoices):
        HR_INTERVIEW = 'HR', 'HR Собеседование'
        HR_REJECTED = 'HR_NO', 'Не прошел HR'
        TECH_INTERVIEW = 'TECH', 'Тех. Собеседование'
        TECH_REJECTED = 'TECH_NO', 'Не прошел тех.собес'
        FINAL_REVIEW = 'FINAL', 'На рассмотрении'
        HIRED = 'HIRED', 'Принят'
        REJECTED = 'REJECTED', 'Отклонен'

    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='candidates')
    full_name = models.CharField('ФИО', max_length=200)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20, blank=True)
    status = models.CharField(
        'Статус',
        max_length=10,
        choices=Status.choices,
        default=Status.HR_INTERVIEW
    )
    hr_comment = models.TextField('Комментарий HR', blank=True)
    tech_comment = models.TextField('Комментарий тех.спеца', blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name='Кто добавил',
        related_name='added_candidates'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} ({self.get_status_display()})'