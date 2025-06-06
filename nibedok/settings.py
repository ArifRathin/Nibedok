"""
Django settings for nibedok project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
# import django
# django.setup()
from pathlib import Path
import os
from os.path import normpath, join

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^tqr&cu9by*ko9&@4a@x)nzv+-q9bbyoexns@#niij56k&+%%8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'useraccounts.User'

# Application definition

INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'useraccounts',
    'country',
    'seller_offer',
    'buyer_post',
    'product',
    'inbox',
    'notification'
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

ROOT_URLCONF = 'nibedok.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR,'templates'],
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

WSGI_APPLICATION = 'nibedok.wsgi.application'
ASGI_APPLICATION = 'nibedok.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nibedok',
        'USER': 'postgres',
        # 'PASSWORD': 'rathin',
        'PASSWORD': 'rathin2025',
        # 'HOST': 'localhost',
        'HOST': 'nibedok.cpki84qomvcq.eu-north-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_ROOT = normpath(join(BASE_DIR, 'staticfiles'))

STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     BASE_DIR,'static'
# ]
STATICFILES_DIRS = (
    normpath(join(BASE_DIR, 'static')),
)

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # "hosts": [("127.0.0.1", 6379)],
            "hosts": [("16.171.41.180", 6379)],
            # "hosts": [("nibedok-redis-3vrzgs.serverless.eun1.cache.amazonaws.com", 6379)],
        },
    },
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 20*1024*1024
MAX_UPLOAD_LIMIT = 4*1024*1024

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "ecc.eagle@gmail.com"
EMAIL_HOST_PASSWORD = "omcevrvteokwqvkq"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_BROKER_URL = 'redis://16.171.41.180:6379/0'
# CELERY_BROKER_URL = 'redis://nibedok-redis-3vrzgs.serverless.eun1.cache.amazonaws.com:6379/0'
CELERY_TIMEZONE = 'Asia/Dhaka'