import os
from .base import *

DEBUG = True

# ADMINS = [
#  ('Antonio M', 'email@mydomain.com'),
# ]

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}

REDIS_URL = 'redis://redis:6379'
CACHES['default']['LOCATION'] = REDIS_URL