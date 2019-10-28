from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta
from dealflowbox.task import update_date
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onspace.settings')

app = Celery('proj')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# REFERENCE: https://www.revsys.com/tidbits/celery-and-django-and-docker-oh-my/
# Celerybeat 태스크 추가/정의
from celery.schedules import crontab

app.conf.beat_schedule = {
    'update_check': {
        'task': 'dealflowbox.task.update_date',
        'schedule': crontab(minute='0', hour='9', day_of_week='mon-fri'),
        'args': (),
    },
}
