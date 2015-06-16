__author__ = 'andriyg'

# noinspection PyUnresolvedReferences
from .base import *

DEBUG = bool_env('DJANGO_DEBUG', True)
TEMPLATE_DEBUG = DEBUG
ENABLE_MEDIA = DEBUG or bool_env('DJANGO_FORCE_MEDIA', True)

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INTERNAL_IPS = ('127.0.0.1', '::1',)
INSTALLED_APPS += ('debug_toolbar',)
