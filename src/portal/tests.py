from django.test import TestCase

# Create your tests here.

def method_test():
    pass


class Case1(TestCase):
    # noinspection PyPep8Naming
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

    def method_2_test(self):
        pass
