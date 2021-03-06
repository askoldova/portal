import os
import re
from django.conf import settings
from django.contrib.sites.models import Site
import filebrowser
from django.core.urlresolvers import reverse
from filebrowser import functions as fbfunctions

import core
from . import models, objects

__author__ = 'andriy'

_PROTOCOL_RE = re.compile(r'^(\w+:)?//')


def _load_language_and_locale(lang, l10n_lang):
    core.check_exist_and_type2(lang, objects.Language)
    core.check_type2(l10n_lang, objects.Language)

    olang = objects.Language(code=lang.code, name=lang.caption, name_i18n=lang.caption)
    if not l10n_lang:
        l10n_lang = olang
    try:
        l10n_lang = models.Lang.objects.get_by_code(l10n_lang.code)
        locale = models.LangLocale.objects.get_lang_locale(lang=lang, locale=l10n_lang)
        olang = olang.replace_i18n_name(locale.caption)
    except (models.Lang.DoesNotExist, models.Lang.MultipleObjectsReturned,
            models.LangLocale.DoesNotExist, models.LangLocale.MultipleObjectsReturned):
        pass
    return olang


def _submenu_item_ref(lang, menu_item, main_menu_ref):
    core.check_exist_and_type2(objects.Language, lang=lang)
    core.check_exist_and_type2(models.MenuItem, menu=menu_item)
    core.check_exist_and_type2(objects.MenuRef, main_menu_ref=main_menu_ref)
    try:
        i = models.MenuItemI18n.objects.by_code_and_lang(menu_item.id, lang.lower_code)
        caption = i.caption
    except models.MenuItemI18n.DoesNotExist:
        caption = menu_item.caption
    return objects.MenuItemRef(code=menu_item.id, slug=menu_item.slug, menu=main_menu_ref, title=caption, lang=lang)


def _main_menu_ref(language, main_menu, subitems):
    """
    :type language: portal.objects.Language
    :type main_menu: portal.models.MainMenu
    :rtype: portal.objects.MenuRef
    """
    core.check_exist_and_type2(objects.Language, language=language)
    core.check_exist_and_type2(models.MainMenu, menu_item=main_menu)
    try:
        i = models.MainMenuI18n.objects.by_code_and_lang(main_menu.id, language.lower_code)
        caption = i.caption
    except models.MainMenuI18n.DoesNotExist:
        caption = main_menu.caption
    main_menu = objects.MenuRef(main_menu.id, caption, main_menu.width, subitems)
    return main_menu


class PortalService(object):
    def __init__(self):
        pass

    # def __init__

    # noinspection PyMethodMayBeStatic
    def get_current_site_domain(self):
        return Site.objects.get_current().domain

    # def get_current_site_domain

    # noinspection PyMethodMayBeStatic
    def full_url(self, url, site_id=None):
        """
        :type url str
        :type site_id int
        :rtype str
        """
        url = url or ''
        if site_id:
            site = Site.objects.get(id=site_id)
        else:
            site = Site.objects.get_current()

        if _PROTOCOL_RE.match(url):
            return url

        if not _PROTOCOL_RE.match(site.domain):
            prefix = u"http://"
        else:
            prefix = u""

        _url = prefix + site.domain
        if _url.endswith('/') and url.startswith('/'):
            _url += url[1:]
        elif not _url.endswith('/') and not url.startswith('/'):
            _url += '/' + url
        else:
            _url += url
        return _url
    # def full_url

    def resolve_to_full_url(self, view_name, site_id=None, *args, **kwargs):
        return self.full_url(reverse(view_name, args=args, kwargs=kwargs), site_id)
    # def full_url

    """
    Returns full url of 'gallery' version image
    """
    def url_of_gallery_image_version(self, image_path):
        """
        :type image_path: basestring
        :return: unicode
        """
        return self.url_of_image_version(image_path, 'gallery')
    # end url_of_gallery_image_version

    def url_of_image_version(self, image_path, version):
        """
        :type image_path: basestring
        :type version: basestring
        :return: unicode
        """
        if not image_path or not isinstance(image_path, basestring):
            raise ValueError('image_path is null or not string')

        location = fbfunctions.get_version_path(fbfunctions.url_to_path(image_path), '')
        gallery_path = fbfunctions.version_generator(location, version)
        if not gallery_path:
            raise ValueError("invalid image %s" % (image_path,))
        return self.full_url(fbfunctions.path_to_url(gallery_path))
    # end url_url_of_image_version

    def set_entity_filebrowser_path(self, entity_name, *args):
        values = [entity_name]
        values.extend(args)

        values = [str(v).replace("//", "/").replace(".", "_") for v in values]

        path = os.path.join(settings.MEDIA_ROOT, settings.FILEBROWSER_DIRECTORY,
                            *values)
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except os.error:
                pass
        # if os.path

        filebrowser.set_default_dir('/'.join(values))
    # set_entity_filebrowser_path

    def generate_view(self, url, view, do_not_store=False, *args, **kwargs):
        if not isinstance(view, callable):
            raise ValueError("%s passed view is not a callable" % (view,))
        if not isinstance(url, basestring):
            raise ValueError("%s passed url is not a string" % (url,))
        result = view(None, *args, **kwargs)
        if do_not_store:
            return

        if url.endswith("/"):
            url += "/index.html"

        url.split("/")
    # def generate_view

    def get_language_locale(self, lang, i10n_lang=None):
        """
        :type lang: portal.models.Lang
        :type i10n_lang: portal.objects.Language
        :rtype: portal.objects.Language
        """
        if not lang or not isinstance(lang, models.Lang):
            raise ValueError("lang [%s] is empty or not portal.models.Lang" % (lang,))

        if i10n_lang and not isinstance(i10n_lang, objects.Language):
            raise ValueError("base_lang %s is not object.Language" % (lang,))

        return _load_language_and_locale(lang, i10n_lang)

    # def get_language

    def get_language(self, lang, i10n_lang=None):
        """
        :type lang: basestring
        :type i10n_lang: portal.objects.Language
        :rtype: portal.objects.Language
        """
        if not lang or not isinstance(lang, basestring):
            raise ValueError("lang %s is empty or not string" % (lang,))

        if i10n_lang and not isinstance(i10n_lang, objects.Language):
            raise ValueError("base_lang %s is not object.Language" % (lang,))

        try:
            lang = models.Lang.objects.get_by_code(code=lang.upper())
        except models.Lang.DoesNotExist or models.Lang.MultipleObjectsReturned:
            return objects.Language.LANGUAGE_NOT_FOUND

        return _load_language_and_locale(lang, i10n_lang)

    # def get_language

    def get_default_language(self):
        try:
            lang = models.Lang.objects.get_default()
            return self.get_language(lang.code)
        except (models.Lang.DoesNotExist, models.Lang.MultipleObjectsReturned):
            return objects.Language.LANGUAGE_NOT_FOUND

    # def get_default_language

    def get_languages(self, l10n_lang):
        if not l10n_lang or not isinstance(l10n_lang, objects.Language):
            raise ValueError("Localisation code [] is not a language".format(l10n_lang))
        return tuple(_load_language_and_locale(lang, l10n_lang)
                     for lang in models.Lang.objects.all())

    # def get_languages

    def menu_item(self, lang_code, subcategory_code, slug):
        core.check_exist_and_type(lang_code, "lang_code", str, unicode)
        core.check_type(subcategory_code, "subcategory_code", long, int)
        core.check_type(slug, "slug", str, unicode)
        if not slug and not subcategory_code:
            raise ValueError("slug or subcategory_code have to be set")

        lang = self.get_language(lang_code)
        try:
            if slug:
                m = models.MenuItem.objects.by_slug(slug)
            else:
                m = models.MenuItem.objects.by_code(subcategory_code)

            return _submenu_item_ref(lang, m, _main_menu_ref(lang, m.menu, ()))
        except models.MenuItem.DoesNotExist:
            return objects.MENU_ITEM_NOT_EXIST

    def main_menu(self, language):
        """
        :type language: portal.objects.Language
        """
        core.check_exist_and_type2(objects.Language, language=language)

        main_menu_item = objects.MenuRef(-1, "None", 0, ())
        menu = ()
        for menu_item in models.MenuItem.objects.main_menu_items():
            if main_menu_item.code != menu_item.menu.id:
                if main_menu_item.code > -1:
                    menu += (main_menu_item,)
                main_menu_item = _main_menu_ref(language, menu_item.menu, ())
            submenu_item = _submenu_item_ref(language, menu_item, main_menu_item)
            main_menu_item = main_menu_item.add_subitem(submenu_item)

        if main_menu_item.code > -1:
            menu += (main_menu_item,)

        return menu

    def main_menu_items(self, language):
        """
        :type language: portal.objects.Language
        :rtype: tuple[portal.objects.MenuRef]
        """
        core.check_exist_and_type2(objects.Language, language=language)

        menu = ()
        for s in models.MainMenu.objects.all():
            menu += (_main_menu_ref(language, main_menu=s, subitems=()),)

        return menu

    def menu_items(self, language):
        """
        :type language: portal.objects.Language
        :rtype: tuple[portal.object.MenuRef]
        """
        core.check_exist_and_type2(objects.Language, language=language)

        main_menu_item = objects.MenuRef(-1, "None", 0, ())
        menu_items = ()
        for menu_item in models.MenuItem.objects.all():
            if main_menu_item.code != menu_item.menu.id:
                main_menu_item = _main_menu_ref(language, menu_item.menu, ())
            menu_items += (_submenu_item_ref(language, menu_item, main_menu_item),)

        return menu_items
# class PortalService
