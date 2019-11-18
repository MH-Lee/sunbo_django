import os
from celery import Celery
from datetime import timedelta
# from dealflowbox.tasks import update_date
from information.tasks import rescue_data_send, dart_data_send
from news.tasks import professor_data_send, news_datasend

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
    # 'dfb_update_check': {
    #     'task': 'dealflowbox.tasks.update_date',
    #     'schedule': crontab(minute='45', hour='1', day_of_week='mon'),
    #     'args': (),
    # },
    'dart_update': {
        'task': 'news.tasks.dart_data_send',
        'schedule': crontab(minute='45', hour='0', day_of_week='mon'),
        'args': (),
    },
    'rescue_update': {
        'task': 'news.tasks.rescue_data_send',
        'schedule': crontab(minute='00', hour='1', day_of_week='mon'),
        'args': (),
    },
    'news_update': {
        'task': 'news.tasks.rescue_data_send',
        'schedule': crontab(minute='15', hour='1', day_of_week='mon'),
        'args': (),
    },
    'prof_update': {
        'task': 'news.tasks.rescue_data_send',
        'schedule': crontab(minute='30', hour='1', day_of_week='mon'),
        'args': (),
    },
}
