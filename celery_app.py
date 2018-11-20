from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

if os.getenv('ENV') == 'PRODUCTION':
    config_settings = "config.settings.prod"
else:
    config_settings = "config.settings.local"

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', config_settings)
app = Celery('flightbooking')


app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))