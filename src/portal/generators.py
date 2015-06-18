from . import views
import generation as gen
from portal.models import DefaultPageGenerate, IndexPageGenerate

__author__ = 'andriy'

def accept_and_generate(command):
    if isinstance(command, IndexPageGenerate):
        return gen.save_generation(views.generate_index(views.index_url()))
    elif isinstance(command, DefaultPageGenerate):
        return gen.save_generation(views.generate_default(
            views.default_url(command.language_code), command.language_code))

    return False


