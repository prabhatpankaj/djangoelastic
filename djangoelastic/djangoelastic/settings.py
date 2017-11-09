import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False

import key

SECRET_KEY = key.SECRET_KEY

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoelastic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'djangoelastic.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    if 'RDS_DB_NAME' in os.environ:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ['RDS_DB_NAME'],
                'USER': os.environ['RDS_USERNAME'],
                'PASSWORD': os.environ['RDS_PASSWORD'],
                'HOST': os.environ['RDS_HOSTNAME'],
                'PORT': os.environ['RDS_PORT'],
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'ebdb',
                'USER': 'djangoelastic',
                'PASSWORD': 'djangoelastic',
                'HOST': 'aapgzjsi8br2ry.cq88san07kjj.us-east-1.rds.amazonaws.com',
                'PORT': '3306',
                'OPTIONS': {
                    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                }
            }
        }



STATIC_URL = '/static/'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles")]
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES[0]['DIRS'] = [
    TEMPLATES_DIR,
]

INSTALLED_APPS += [
    'django.contrib.sites',
    'storages',
    'main',
    'publisher',
    'django_celery_beat'
]

SITE_ID = 1

AUTH_USER_MODEL = 'main.User'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

DEFAULT_EMAIL_USER = key.DEFAULT_EMAIL_USER
SERVER_EMAIL = key.SERVER_EMAIL
EMAIL_HOST = key.EMAIL_HOST
EMAIL_PORT = 587
EMAIL_HOST_USER = key.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = key.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = True
    
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

if DEBUG:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn')
    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media_cdn')
    MEDIA_URL = '/media/'
else:
    AWS_ACCESS_KEY_ID = key.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = key.AWS_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = key.AWS_STORAGE_BUCKET_NAME
    AWS_CLOUDFRONT_DOMAIN = key.AWS_CLOUDFRONT_DOMAIN
    
    STATICFILES_LOCATION = 'static'
    STATICFILES_STORAGE = 'djangoelastic.storage.StaticStorage'
    STATIC_URL = "https://%s/%s/" % (AWS_CLOUDFRONT_DOMAIN, STATICFILES_LOCATION)
    MEDIAFILES_LOCATION = 'media'
    MEDIA_URL = "https://%s/%s/" % (AWS_CLOUDFRONT_DOMAIN, MEDIAFILES_LOCATION)
    DEFAULT_FILE_STORAGE = 'djangoelastic.storage.MediaStorage'

if DEBUG:
    # REDIS related settings 
    REDIS_HOST = 'localhost'
    REDIS_PORT = '6379'
    BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
    BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600} 
    CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
else:
    CELERY_BROKER_TRANSPORT = 'sqs'
    CELERY_BROKER_TRANSPORT_OPTIONS = {
        'region': 'us-east-1',
    }
    CELERY_BROKER_USER = key.AWS_ACCESS_KEY_ID
    CELERY_BROKER_PASSWORD = key.AWS_SECRET_ACCESS_KEY
    CELERY_WORKER_STATE_DB = '/var/run/celery/worker.db'
    CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
    CELERY_WORKER_PREFETCH_MULTIPLIER = 0         # See https://github.com/celery/celery/issues/3712
    
    CELERY_DEFAULT_QUEUE = 'celery'
    CELERY_QUEUES = {
        CELERY_DEFAULT_QUEUE: {
            'exchange': CELERY_DEFAULT_QUEUE,
            'binding_key': CELERY_DEFAULT_QUEUE,
        }
    }

