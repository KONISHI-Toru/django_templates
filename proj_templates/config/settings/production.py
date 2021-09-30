from .settings import *


SECRET_KEY = env('DJANGO_SECRET_KEY')

DEBUG = False

STATIC_ROOT = '/static'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'thnmaster0@gmail.com'
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = env('SMTP_PASSWORD')
