from .base import *

DEBUG = False

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME'),
        'USER':  os.getenv('DB_USER') ,
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost'
    }
}