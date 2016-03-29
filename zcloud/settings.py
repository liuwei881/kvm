"""
Django settings for zcloud project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEDIA_ROOT = '/data/py/zxrCloud/images'
LOGIN_URL = '/'

SECRET_KEY = '7r*=$m3ad*^l3vjy1lm-#akg^5ut8@#do+qtdcmr0)q65n+t*0'
DEBUG = True 

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*',]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'autopform',
    'manager_kvm',
    'debugtools',
    'webkvm',
    'djcelery',
    'users',
    'django_crontab',
    'clouddisk',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'zcloud.urls'

WSGI_APPLICATION = 'zcloud.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zcloud',
        'USER': 'root',
        'PASSWORD':'QX9rX8UY50gznYo',
        'HOST':'127.0.0.1',
        'PORT':'3306',
    }
}

LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/assets/'
STATICFILES_DIRS = (
        '/data/py/zxrCloud/assets/',
)

#CRONJOBS = (
#    ('*/5 * * * *', 'manager_kvm.cron.monitor_kvm_status'),
#)
import djcelery
djcelery.setup_loader()
CELERY_IMPORTS = ('manager_kvm.tasks')