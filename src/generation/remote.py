import imp
from django.apps import apps
from _celery.celery import app

__author__ = 'andriyg'

_logger = app.log.get_default_logger(__file__)

_modules = ()
def _load_modules_int(logger):
    modules = set()
    for app in apps.get_app_configs():
        if hasattr(app.module, 'generators'):
            generators = getattr(app.module, 'generators')
            if hasattr(generators, 'accept_and_generate'):
                modules.add(generators)
                continue
        logger.info("Application %s contain no generator " % (app.label,))

    return tuple(modules)
# def _load_modules_int

def _load_modules():
    global _modules
    if not _modules:
        _modules = _load_modules_int(logger=_logger)
        _logger.info("Loaded modules generators %s" % (_modules,))

    return _modules

# def _load_modules

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


