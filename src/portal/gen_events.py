import collections

__author__ = 'andriyg'

class SiteRegenerate(collections.namedtuple("SiteRegenerate", ())):
    pass

class DefaultPageGenerate(collections.namedtuple("DefaultPageGenerate", "language_code")):
    def __new__(cls, language_code):
        if not language_code:
            raise ValueError("LanguageCode is not specified")
        return super(DefaultPageGenerate, cls).__new__(cls, language_code=language_code)

    # def __new__
# class DefaultPageGenerate

IndexPageGenerate = collections.namedtuple("IndexPageGenerate", ())
