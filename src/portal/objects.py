__author__ = 'andriy'

from collections import namedtuple


class Language(namedtuple("Language", "code name name_i18n lower_code")):
    LANGUAGE_NOT_FOUND = None

    def __new__(cls, code, name, name_i18n):
        return super(Language, cls).__new__(cls, code, name, name_i18n, code.lower())


# class Language

Language.LANGUAGE_NOT_FOUND = Language(code="NA", name="Not available", name_i18n="Not available")
LANGUAGE_NOT_FOUND = Language.LANGUAGE_NOT_FOUND


class MenuItemRef(namedtuple("MenuItemRef", "code title language")):
    def __new__(cls, code, title, language):
        return super(MenuItemRef, cls).__new__(cls, code=code, title=title, language=language)


MENU_ITEM_NOT_EXIST = MenuItemRef(0, "Does not exists", LANGUAGE_NOT_FOUND)
