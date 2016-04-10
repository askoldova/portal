import logging
from django.apps import apps
import imp
from django.conf import settings

__author__ = 'andriyg'

_logger = logging.getLogger(__file__)

_modules = ()
def _load_modules_int(logger):
    modules = set()
    for _app in apps.get_app_configs():
        # noinspection PyBroadException
        try:
            if not hasattr(_app.module, 'generators'):
                imp("{}.generator".format(_app.label))
            generators = getattr(_app.module, 'generators')
            if hasattr(generators, 'accept_and_generate'):
                modules.add(generators)
                continue

        except Exception, e:
            logger.warn("Can't check module {} for generators.accept_and_generate".format(_app.label), exc_info=e)

        logger.info("Application %s contain no generator " % (_app.label,))

    return tuple(modules)
# def _load_modules_int

def _load_modules():
    global _modules
    if not _modules:
        _modules = _load_modules_int(logger=_logger)
        _logger.info("Loaded modules generators %s" % (_modules,))

    return _modules

# def _load_modules

def _generate_silent(m, command):
    # noinspection PyBroadException
    try:
        return m.accept_and_generate(command)
    except Exception as e:
        _logger.error("Error generate for %s in %s" % (command, m,), exc_info=e)
        return True

def _generate(m, command):
    return m.accept_and_generate(command)


def schedule_generation(command):
    for m in _load_modules():
        if settings.PAGE_GENERATION_MODE == "remote":
            result = _generate(m, command)
        else:
            result = _generate_silent(m, command)
        if result:
            return True
    # for m in modules

    _logger.warn("Can't generate for: %s" % (command, ))
# def schedule_generation

