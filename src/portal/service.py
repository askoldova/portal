import os
import re
from django.conf import settings
from django.contrib.sites.models import Site
import filebrowser
from filebrowser import functions as fbfunctions
from . import models, objects

__author__ = 'andriy'

_PROTOCOL_RE = re.compile(r'^(\w+:)?//')

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
        return self.full_url(self.reverse(view_name, args=args, kwargs=kwargs), site_id)
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

    def get_language(self, lang, base_lang=None):
        """
        :type lang: basestring
        :type base_lang: portal.objects.Language
        :rtype: portal.objects.Language
        """
        if not lang or not isinstance(lang, basestring):
            raise ValueError("lang %s is empty or not string" % (lang,))

        if base_lang and not isinstance(base_lang, objects.Language):
            raise ValueError("base_lang %s is not object.Language" % (lang,))

        try:
            lang = models.Lang.objects.get_by_code(code=lang.upper())
        except models.Lang.DoesNotExist or models.Lang.MultipleObjectsReturned:
            return objects.Language.LANGUAGE_NOT_FOUND

        olang = objects.Language(code=lang.code, name=lang.caption, name_i18n=lang.caption)
        if not base_lang:
            base_lang = olang
        try:
            base_lang = models.Lang.objects.get_by_code(base_lang.code)
            locale = models.LangLocale.objects.get_lang_locale(lang=lang, locale=base_lang)
            olang = olang._replace(name_i18n=locale.caption)
        except models.Lang.DoesNotExist or models.Lang.MultipleObjectsReturned or \
                models.LangLocale.DoesNotExist or models.LangLocale.MultipleObjectsReturned:
            pass

        return olang

    # class get_language

    def get_default_language(self):
        try:
            lang = models.Lang.objects.get_default()
            return self.get_language(lang.code)
        except models.Lang.DoesNotExist or models.Lang.MultipleObjectsReturned:
            return objects.Language.LANGUAGE_NOT_FOUND

# class PortalService


class PublicationsService(object):
    def __init__(self, portal_service=PortalService()):
        """
        :type portal_service: portal.service.PortalService
        """
        super(PublicationsService, self).__init__()
        self.portal_service = portal_service
    # def __init__

    def get_publication_item_by_id(self, id, lang):
        """
        :type id: long
        :type lang: portal.objects.language
        :rtype: publication: portal.objects.PublicationView
        """
        id = long(id)
        if not id:
            raise ValueError("Publication ID is not set")
        if not lang or not isinstance(lang, objects.Language):
            raise ValueError("Lang [%s] is not a Language")

    # def get_publication_item_by_id

# class PublicationsService
