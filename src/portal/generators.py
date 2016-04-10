import logging

from django.conf import settings

import generation as gen
from portal import gen_events
from . import views

__author__ = 'andriy'

_logger = logging.getLogger(__file__)


def generate_site():
    apply_internal(gen_events.DefaultPageGenerate)


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
