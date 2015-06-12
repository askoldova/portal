from . import views
import collections
import generation as gen

__author__ = 'andriy'

class DefaultPageGenerate(collections.namedtuple("DefaultPageGenerate", "language_code")):
    def __new__(cls, language_code):
        return super(DefaultPageGenerate, cls).__new__(cls, language_code)


# end DefaultPageGenerate

def accept_and_generate(command):
    if isinstance(command, IndexPageGenerate):
        return gen.save_generation(views.generate_index(views.index_url()))
    elif isinstance(command, DefaultPageGenerate):
        return gen.save_generation(views.generate_default(
            views.default_url(command.language_code), command.language_code))

    return False


class IndexPageGenerate(object):
    pass