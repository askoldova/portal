from . import views
import logging
from django.conf import settings
import generation as gen
from _celery.celery import app
from portal import gen_events

__author__ = 'andriy'


if settings.PAGE_GENERATION_MODE == "remote":
    _logger = app.log.get_default_logger(__file__)
else:
    _logger = logging.getLogger(__file__)


def generate_site():
    apply_internal(gen_events.DefaultPageGenerate)

@app.task(name="portal.generators._generate_internal")
def _generate_internal(command1):
    accept_and_generate(command1)

def apply_internal(command):

    if not settings.PAGE_GENERATION_MODE:
        accept_and_generate(command)
    else:
        _generate_internal.apply_async((command,))
# def apply_internal

def accept_and_generate(command):
    if isinstance(command, gen_events.SiteRegenerate):
        generate_site()
        # Site regenerate is a cascade event, have to be handled by all modules
        return False
    if isinstance(command, gen_events.IndexPageGenerate):
        return gen.save_generation(views.generate_index(views.index_url()))

    return False


