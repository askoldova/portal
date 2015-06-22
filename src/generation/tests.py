import logging
from django.conf import settings
from django.test import TestCase


class GeneratorsDetectTest(TestCase):
    def __init__(self, methodName='runTest'):
        super(GeneratorsDetectTest, self).__init__(methodName)

    def test_detect(self):
        logger = logging.getLogger(__file__)
        from . import remote
        installed_modules = remote._load_modules_int(logger)
        logger.info("Loaded modules generators %s" % (installed_modules,))
        self.assertEqual(len(installed_modules), 2)
