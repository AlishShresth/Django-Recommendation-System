import os
from celery import Celery

# initialize Celery app
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "recommendation_system_django.production")
app = Celery("movies")
# configure Celery to use Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")
# automatically discover and register Celerytasks
app.autodiscover_tasks()
