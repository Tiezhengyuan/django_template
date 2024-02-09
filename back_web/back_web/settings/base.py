"""
Django settings for back_web project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from dotenv import load_dotenv
load_dotenv()
from pathlib import Path
from celery.schedules import crontab



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lel_6thr+^a)4*usqi1q*e0q8i&g9ug5rag2%7q*jqe2&lk*96'


# Application definition

INSTALLED_APPS = [
    # default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # required by allauth
    'django.contrib.sites',
    
    # customary app
    'accounts',
    'reporting',

    # CSS
    'bootstrap5',
    # third-party authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    #asynchronous tasks
    'django_celery_results',
    'django_celery_beat',
    # TODO: confirm that in admin
    # 'redis_admin',
]

SITE_ID = 1

AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    # thirth-party authentication
    "allauth.account.auth_backends.AuthenticationBackend",
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #third-party authentication
    "allauth.account.middleware.AccountMiddleware",  
]

ROOT_URLCONF = 'back_web.urls'


# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    # redirect URI: http://localhost:8000/accounts/google/login/callback/
    'google': {
        'APP': {
            'client_id': str(os.environ.get('GOOGLE_CLIENT_ID')),
            'secret': str(os.environ.get('GOOGLE_SECRET')),
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'EMAIL_AUTHENTICATION': True,
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = 'static/'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'back_web.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# cache
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

# # https://redis-py.readthedocs.io/en/latest/index.html#redis.Redis
# REDIS_SERVERS = dict(
#     redis_server=dict(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB),
# )


# asynchronous tasks
# broker of Celery task 
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
# results are displayed in Admin
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

# define scheduled tasks
CELERY_BEAT_SCHEDULE = {
    'test_scheduled_task': {
        'task': 'reporting.tasks.test_task',
        # run task per 30 seconds
        # 'schedule': 30.0,
        # cronjob per 2 hours
        "schedule": crontab(hour="1", day_of_week="*"),
        'args': (16, 16),
        'options': {
            'expires': 15.0,
        },
    },
}

