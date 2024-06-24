from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RecommendSystem')

app = Celery('RecommendSystem')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
#Реализация Celerbeat отправляет письмо каждое утро в 8:00
app.conf.beat_schedule = {
    'send-daily-email-every-morning': {
        'task': 'qa_app.tasks.send_daily_email',
        'schedule': crontab(),
        # 'schedule': crontab(hour=4, minute=30),
    },
}