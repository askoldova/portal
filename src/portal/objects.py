import core

__author__ = 'andriy'

from collections import namedtuple


class Language(namedtuple("Language", "code name name_i18n lower_code")):
    LANGUAGE_NOT_FOUND = None

    def __new__(cls, code, name, name_i18n):
        return super(Language, cls).__new__(cls, code, name, name_i18n, code.lower())

    def replace_i18n_name(self, name_i18n):
        return self._replace(name_i18n=name_i18n)
# class Language

Language.LANGUAGE_NOT_FOUND = Language(code="NA", name="Not available", name_i18n="Not available")
LANGUAGE_NOT_FOUND = Language.LANGUAGE_NOT_FOUND


class MenuRef(namedtuple("MenuRef", "code title width items")):
    def __new__(cls, code, title, width, items):
        width = long(width) if width else None
        core.check_int(code=code)
        core.check_string_value(title=title)
        core.check_type2(tuple, items=items)

        return super(MenuRef, cls).__new__(cls, code=code, title=title, items=items, width=width or 0)

    def add_subitem(self, submenu_item):
        core.check_exist_and_type2(MenuItemRef, submenu_item=submenu_item)

        return MenuRef(self.code, self.title,  self.width, self.items + (submenu_item,))

MENU_NOT_EXIST = MenuRef(0, "Does not exists", 0, ())


class MenuItemRef(namedtuple("MenuItemRef", "code slug title menu language")):
    def __new__(cls, lang, code, slug, title, menu):
        return super(MenuItemRef, cls).__new__(cls, code=code, slug=slug, title=title, language=lang, menu=menu)


MENU_ITEM_NOT_EXIST = MenuItemRef(0, None, "Does not exists", LANGUAGE_NOT_FOUND, MENU_NOT_EXIST)

