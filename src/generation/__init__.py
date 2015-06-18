import codecs
import collections
import os

from django.conf import settings

from _celery.celery import app

__author__ = 'andriy'


class GenerationResult(collections.namedtuple("GenerationResult", "url content")):
    @staticmethod
    def __new__(cls, url, content):
        """
        :type url: basestring
        :type content: basestring
        """
        return super(GenerationResult, cls).__new__(cls, url, content)

    # def __new__
# def GenerationResult

_modules = ()
@app.task()
def schedule_generation(command):
    logger = app.log.get_default_logger(__file__)

    global _modules
    if not _modules:
        def try_import(module):
            try:
                return __import__("%s.generators" % (module,))
            except ImportError:
                return None

        modules = (try_import(f) for f in settings.INSTALLED_APPS)
        _modules = tuple(f for f in modules if f)
        logger.info("Loaded modules generators %s" % (_modules,))

    # noinspection PyBroadException
    try:
        for m in _modules:
            if m.accept_and_generate(command):
                return
    except Exception as e:
        logger.exception("Error generate for: %s, %s" % (command, e, ))
        return

    logger.exception("Can't generate for: %s" % (command, ))

def save_generation(generation):
    """
    :type generation: generation.GenerationResult
    :rtype: bool
    """
    if not generation or not isinstance(generation, GenerationResult):
        raise ValueError("%s generation is empty or not GenerationResult" % (generation))

    url = generation.url
    if url.endswith("/") or not url.endswith(".html") or not url.endswith(".htm"):
        url += "/index.html"

    parts = [f for f in url.split('/') if f]
    path = os.path.join(settings.MEDIA_ROOT, *parts[:-1])
    file_name = os.path.join(settings.MEDIA_ROOT, *parts)
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == 17:  # file exist
            pass
        else:
            raise e
    f = codecs.open(file_name, mode="w", encoding="utf-8")
    try:
        f.write(generation.content)
        f.flush()
    finally:
        f.close()

    return True

# def save_generation
