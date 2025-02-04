import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'recommendation_system_django.production')

application = get_wsgi_application()
