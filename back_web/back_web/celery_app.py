


import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_web.settings')

app = Celery('back_web', broker=settings.CELERY_BROKER_URL)
app.config_from_object('django.conf.settings', namespace='CELERY')
app.autodiscover_tasks()

