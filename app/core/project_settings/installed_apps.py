<<<<<<< HEAD
from dotenv import load_dotenv
import os

load_dotenv()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

#ckeditor
    'ckeditor',
    'ckeditor_uploader',
    'django_resized',
#apps
    'apps.cms',
    'apps.contacts',
    'apps.extra',
=======
from dotenv import load_dotenv
import os

load_dotenv()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

#ckeditor
    'ckeditor',
    'ckeditor_uploader',
    'django_resized',
#apps
    'apps.cms',
    'apps.contacts',
    'apps.extra',
>>>>>>> 3da9a24fed32cd4ff816f1cc31908e8e39f2cc4a
]