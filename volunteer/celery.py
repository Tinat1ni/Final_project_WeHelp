from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'volunteer.settings')

app = Celery('volunteer')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-expired-posts-once-a-day': {
        'task': 'post.tasks.delete_expired_posts',
        'schedule': crontab(hour=0, minute=0),  # Run every day at midnight (00:00)
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

