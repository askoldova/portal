import imp
from django.conf import settings
from _celery.celery import app

__author__ = 'andriyg'

_logger = app.log.get_default_logger(__file__)

_modules = ()
def _load_modules():
    global _modules
    if not _modules:
        def try_import(module):
            module_name = "%s.generators" % (module,)
            try:
                imp.find_module(module_name)
                loaded = imp.load_module(module_name)
                return loaded
            except ImportError:
                _logger.info("Can't load %s module" % (module_name,))
            return None

        modules = tuple(try_import(f) for f in settings.INSTALLED_APPS)
        _modules = tuple(f for f in modules if f and f)
        _logger.info("Loaded modules generators %s" % (_modules,))

    return _modules

def schedule_generation(command):

    for m in _load_modules():
        # noinspection PyBroadException
        try:
            if m.accept_and_generate(command):
                return
        except Exception as e:
            _logger.exception("Error generate for %s in %s" % (command, m,), exc_info=e)
            return
    # for m in modules

    _logger.error("Can't generate for: %s" % (command, ))
