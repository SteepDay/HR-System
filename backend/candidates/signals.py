from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Candidate

@receiver(post_save, sender=Candidate)
def send_status_notification(sender, instance, **kwargs):
    if kwargs.get('created', False):
        return  # Пропускаем создание новой записи
    
    # Получаем предыдущее состояние
    prev_status = None
    if hasattr(instance, '_pre_save_status'):
        prev_status = instance._pre_save_status
    
    # Проверяем, изменился ли статус
    if prev_status != instance.status:
        subject = f"Обновление статуса по вакансии {instance.vacancy.title}"
        
        context = {
            'candidate': instance,
            'prev_status': prev_status,
            'new_status': instance.status,
            'vacancy': instance.vacancy
        }
        
        html_message = render_to_string('candidates/email/status_change.html', context)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject,
            plain_message,
            None,  # Используется DEFAULT_FROM_EMAIL
            [instance.email],
            html_message=html_message,
            fail_silently=False
        )