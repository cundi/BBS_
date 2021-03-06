# -*- coding: utf-8 -*-
"""
Django settings for BBS project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')==dyq#xbj*2u3ch9r89tf5(!duh-6@lolz^d2k@5=i#59b!^@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'accounts',
    'bb',
    'tool_bar',
    'pagination',
    'DjangoUeditor',
    'utils.templatetags',
    'debug_toolbar',
    'utils',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'MixBBS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',
                'django.core.context_processors.i18n',
            ],
        },
    },
]


WSGI_APPLICATION = 'MixBBS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/


LANGUAGE_CODE = 'en-US'


TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'static_root')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static', 'static_files'),)

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

MEDIA_URL = '/media/'
# # for ckeditor
# DJANGO_WYSIWYG_FLAVOR = "ckeditor"
#
# CKEDITOR_UPLOAD_PATH = "uploads/"

LOGIN_REDIRECT_URL = '/'

MAX_UPLOAD_SIZE = "524288"

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'love86930@gmail.com'
EMAIL_HOST_PASSWORD = 'x5msTwMNeG2#4^E8'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)


# 如果用户创建账户时，值为真则注册的账户默认为非启用状态，并需要邮件激活
ACCOUNT_APPROVAL_REQUIRED = False

UPLOAD_PATH = os.path.join(BASE_DIR, 'static/upload')

DEFAULT_WEBSITE_URL = "http://www.example.com"

from django.core.files.storage import FileSystemStorage
storage = FileSystemStorage(
    location=UPLOAD_PATH, base_url='/static/upload/')

site_name = u'MixBBS'
logo_name = u'MixBBS'
links = {}
site_off = False