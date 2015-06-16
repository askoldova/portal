# noinspection PyUnresolvedReferences
from .base_tests import *

TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

INSTALLED_APPS += (
    'django_nose',
)


