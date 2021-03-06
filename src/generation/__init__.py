import codecs
import collections
import os

from django.conf import settings

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

def save_generation(generation):
    """
    :type generation: generation.GenerationResult
    :rtype: bool
    """
    if not generation or not isinstance(generation, GenerationResult):
        raise ValueError("%s generation is empty or not GenerationResult" % (generation,))

    if generation == EMPTY_GENERATION:
        return

    url = generation.url or ''
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

EMPTY_GENERATION = GenerationResult('', 'No content')
