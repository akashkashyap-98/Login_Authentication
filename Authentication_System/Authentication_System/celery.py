from  __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Authentication_System.settings')

app = Celery('Authentication_System')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'send-mail-everyday':{
        'task':'send_mail_app.tasks.send_mail_func',
        'schedule': crontab(hour=16, minute=10),
        # 'args':(2,)
    },
    'send-mail-with-attachment':{
        'task':'send_mail_app.tasks.generate_excel_and_send_email',
        'schedule': crontab(hour=16, minute=11),
    }
    
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')