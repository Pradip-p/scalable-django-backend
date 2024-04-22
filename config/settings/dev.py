from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += ['debug_toolbar']

MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

#Database
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME'),
        'USER':  os.getenv('DB_USER') ,
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost'
    }
}