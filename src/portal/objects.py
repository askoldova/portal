__author__ = 'andriy'

from collections import namedtuple

class Language(namedtuple("Language", "code name name_i18n")):
    LANGUAGE_NOT_FOUND = None

    def __new__(cls, code, name, name_i18n):
        return super(Language, cls).__new__(cls, code, name, name_i18n)

# class Language

Language.LANGUAGE_NOT_FOUND = Language(code="NA", name="Not available", name_i18n="Not available")
LANGUAGE_NOT_FOUND = Language.LANGUAGE_NOT_FOUND

