# noinspection PyUnresolvedReferences
from .base import *

DATABASES = dict(
    default=dict(
        NAME=':memory:',
        ENGINE='django.db.backends.sqlite3',
))

SITE_ID = 1


CACHES = dict(
    default=dict(
        BACKEND='django.core.cache.backends.dummy.DummyCache',
))

MEDIA_ROOT = os.path.join(BASE_DIR, "tests/media")
FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT

PAGE_GENERATION_MODE = "none"
