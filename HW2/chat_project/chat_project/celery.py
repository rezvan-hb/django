# quick_publisher/celery.py

import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')

app = Celery('chat_project')
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.autodiscover_tasks(lambda: chat_project.settings.INSTALLED_APPS)
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
