from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail
from Authentication_System import settings
from django.utils import timezone
from datetime import timedelta

@shared_task(bind=True)
def send_mail_func(self):
    user = 'akashkashyap12@mailinator.com'
    #timezone.localtime(users.date_time) + timedelta(days=2)
    
    mail_subject = "Hi! Celery Testing by Akash"
    message = "Hello , My name is akash kashyap and i am testing CELERY send mail functionality"
    to_email = user
    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )
    return "Done" 