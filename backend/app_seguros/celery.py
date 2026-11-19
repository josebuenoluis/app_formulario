import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','app_seguros.settings')

celery_app = Celery('app_seguros')
celery_app.config_from_object('django.conf:settings',namespace='CELERY')
celery_app.autodiscover_tasks()