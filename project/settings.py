"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from geopy import Nominatim

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5l#c31j1aw4lrqg8&ts)uzs+fx-)-)q*c%l7%4pmts4u^f+fu4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #thirdapps
    'rest_framework',
    'rest_framework.authtoken',
    #myapps
    'users',
    'notifications',
    'trips',
    'points',
    'tripcomments',
    'medals'
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

ROOT_URLCONF = 'project.urls'

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 4
}

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tripgame',
        'USER': 'mike',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = "users.User"

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "uploads/")
MEDIA_URL = "/uploads/"


#APP'S PROJECT SETTINGS

LEVELS = (
    ('0', 'New'),
    ('1', 'Noob'),
    ('2', 'Begginer'),
    ('3', 'Junior'),
    ('4', 'Sophomore'),
    ('5', 'Intermediate'),
    ('6', 'Backpacker'),
    ('7', 'Advanced'),
    ('8', 'High Authority'),
    ('9', 'Master'),
    ('10', 'True Traveller'),
)

NOTIFICATION_TYPES = (
    ('0', 'new_follower'),
    ('1', 'new_comment'),
    ('2', 'upgrade_level'),
    ('3', 'trip_verification'),
    ('4', 'trusted_trip'),
    ('5', 'fake_trip_under_investigation'),
    ('6', 'added_to_trip'),
    ('7', 'like_trip')
)

REPORT_LEVELS = (
    ('0', 'None'),
    ('1', 'Investigated'),
    ('2', 'Reported'),
)

TRIP_TYPES = (
    ('0', 'Ski & Snow'),
    ('1', 'Trekking'),
    ('2', 'Cultural'),
    ('3', 'Beach'),
    ('4', 'Party'),
    ('5', 'Festival'),
    ('6', 'Surf'),
    ('7', 'None'),
    ('8', 'Gastronomic'),
)



#Geolocator
geolocator = Nominatim(user_agent="travlin")

