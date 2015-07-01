import datetime
import publications
import publications.views
import utils

__author__ = 'andriyg'

from . import models, objects, STATUS_PUBLISHED, STATUS_HIDDEN
from portal import objects as portal_objs

class UrlsResolver:
    def __init__(self):
        pass

    def get_publication_url(self, language_code, publication_id, publication_date, slug):
        raise NotImplemented()

    def get_old_publication_url(self, lang_code, old_id):
        raise NotImplemented()

# class UrlsResolver


class PublicationService(object):

    def __init__(self, urls_resolver, portal_service):
        """
        :type urls_resolver: publications.services.UrlsResolver
        :type portal_service: portal.services.PortalService
        :return:
        """
        if not urls_resolver:
            raise ValueError("url_resolver is not set")
        super(PublicationService, self).__init__()

        self.urls_resolver = urls_resolver
        self.portal_service = portal_service

    # def __init__

    def get_publication_ref_by_id(self, publication_id):
        """
        Get publication reference by publication_id
        :type publication_id: long
        :rtype:
        """
        publication_id = long(publication_id)
        if not publication_id:
            raise ValueError("Publication ID is not set")

        try:
            pub = models.Publication.objects.get_by_id(publication_id=publication_id)
        except models.Publication.DoesNotExist:
            return objects.PUB_REF_NOT_FOUND

        return self._load_pub_ref(pub)

    # def get_publication_by_id

    def _load_pub_ref(self, pub):
        locale = self.portal_service.get_language_locale(pub.locale)
        url = self.urls_resolver.get_publication_url(language_code=locale.lower_code, publication_id=pub.id,
                                                     publication_date=pub.publication_date, slug=pub.slug)
        return objects.PublicationRef(language=locale, publication_id=pub.id,
                                      old_id=pub.old_id, publication_date=pub.publication_date, slug=pub.slug,
                                      title=pub.title, url=url, status=pub.state)

    # def _load_pub_ref

    def get_last_publications(self, lang, published, page_size):
        """
        :type lang: portal.objects.Language
        :type page_size: long
        :type published: boolean
        :rtype: publications.models.Pager
        """
        if not lang or not isinstance(lang, portal_objs.Language):
            raise ValueError("Language[{}] is not set or not a portal.objects.Language".format(lang))

        pager = models.Publication.objects.pager_and_last_pubs(page_size=page_size, lang_code=lang.code)
        return pager.replace_page(tuple(self._publication_preview(p) for p in pager.page))

    # def get_last_publications

    def get_publications_page(self, lang, page, page_size):
        """
        :type lang: portal.objects.Language
        :type page: long
        :type page_size: long
        :rtype: publications.models.Pager
        """
        if not lang or not isinstance(lang, portal_objs.Language):
            raise ValueError("Language[{}] is not set or not a portal.objects.Language".format(lang))

        if page < 1:
            return objects.PAGE_NOT_FOUND
        pager = models.Publication.objects.pager_and_all_pubs_page(page=page, page_size=page_size, lang_code=lang.code)
        if not pager.page:
            return objects.PAGE_NOT_FOUND
        return pager.replace_page(tuple(self._publication_preview(p) for p in pager.page))

    # def get_publications_page

    def _publication_preview(self, pub):
        if not pub or not isinstance(pub, models.Publication):
            raise ValueError("Publication[{}] is not set or not a portal.models.Publication".format(pub))

        if pub.rss_url and pub.rss_stream:
            url=pub.rss_url
            custom_link_name = pub.rss_stream.link_caption
        else:
            url = self._url_of_publication(pub)
            custom_link_name = None

        return objects.PublicationPreview(url=url, publication_id=pub.id, title=pub.title or '',
                                          custom_link_name=custom_link_name,
                                          short_text=pub.short_text, published=self._is_published(pub),
                                          publication_date=pub.publication_date,
                                          show_date=pub.show_date)

    # def _publication_preview

    def _url_of_publication(self, pub):
        """
        :type pub: publications.models.Publication
        :rtype: basestring
        """
        return self.urls_resolver.get_publication_url(language_code=pub.locale.lower_code,
                                                      publication_id=pub.id,
                                                      publication_date=pub.publication_date,
                                                      slug=pub.slug)
    # def _url_of_publication

    # noinspection PyMethodMayBeStatic
    def _is_published(self, pub):
        """
        :type pub: publications.models.Publication
        :rtype: bool
        """
        if not pub or not isinstance(pub, models.Publication):
            raise ValueError("Publication[{}] is not set or not a portal.models.Publication".format(pub))

        return pub.state in (STATUS_PUBLISHED, STATUS_HIDDEN) and not (pub.rss_url and pub.rss_stream)
    # def _is_published

    def get_all_pubs_new_page_by_old(self, lang, old_page):
        """
        :type lang: portal.objects.Language
        :type old_page: long
        :rtype : long
        """
        if not lang or not isinstance(lang, portal_objs.Language):
            raise ValueError("Language[{}] is not set or not a portal.objects.Language".format(lang))

        if old_page < 1:
            return 0

        conf = models.Configuration.objects.get_configuration()

        old_pages_pager = models.Publication.objects. \
            pager_all_pubs(lang_code=lang.code, page_size=conf.publications_page_size)

        if old_page > old_pages_pager.pages:
            return 0

        return old_pages_pager.pages - old_page + 1

    # def get_all_pubs_new_page_by_old

    def get_publication_ref_by_old_id(self, lang_code, old_id):
        """
        :type lang_code: basestring
        :type old_id: long
        :rtype : publications.objects.PublicationRef
        """
        try:
            publication = models.Publication.objects.get_by_land_and_old_id(lang_code, old_id)
        except models.Publication.DoesNotExist:
            return objects.PUB_REF_NOT_FOUND

        return self._load_pub_ref(publication)
    # def get_publication_ref_by_old_id

    def get_publication_view_by_url(self, lang, year, month, day, slug):
        """
        :type lang: portal.objects.Language
        :type year: long
        :type month: long
        :type day: long
        :param slug: basestring
        :return: publications.objects.PublicationView
        """
        publications.check_exist_and_type(lang, "lang", portal_objs.Language)

        try:
            publication_id = long(slug)
        except ValueError:
            publication_id = None

        try:
            date = datetime.date(year, month, day)
        except ValueError:
            return objects.PUB_NOT_FOUND

        try:
            pub = models.Publication.objects\
                .get_by_lang_date_slug(lang_code=lang.code, publication_date=date,
                                       publication_id=publication_id, slug=slug)
        except models.Publication.DoesNotExist:
            return objects.PUB_NOT_FOUND

        return self._load_publication(lang=lang, pub=pub)

    def _load_publication(self, lang, pub):
        """
        :type lang: portal.objects.Language
        :type pub: publications.models.Publication
        :rtype: publications.objects.PublicationView
        """

        if pub.rss_stream:
            return objects.PUB_NOT_FOUND

        text = pub.text or pub.short_text  # TODO: prepare images placeholders
        return objects.PublicationView(
            pub_date=pub.publication_date,
            show_date=pub.show_date,
            title=pub.title,
            text=text,
            categories=self._publication_categories_refs(pub, lang),
            images=self._publication_images(pub)
        )

    # def _load_publication

    def _publication_categories_refs(self, pub, lang):
        pass

    # def _publication_categories_refs

    def _publication_images(self, pub):
        pass

    # def _publication_images

# class PublicationService
