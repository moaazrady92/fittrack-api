import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') #making sure celery knows django settings

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY') #loading all celery settings
app.autodiscover_tasks() #searchs for tasks.py in every app