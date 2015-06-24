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
            pub = models.Publication.objects.get_by_id(id=publication_id)
        except models.Publication.DoesNotExist:
            return objects.PUBLICATION_NOT_FOUND

        locale = self.portal_service.get_language(pub.locale)
        url = self.urls_resolver.get_publication_url(language_code=locale.lower_code, publication_id=pub.id,
                                                     publication_date=pub.pub, slug=pub.slug)

        return objects.PublicationRef(language_code=locale.lower_code, publication_id=pub.id,
                                      old_id=pub.old_id, publication_date=pub.pub, slug=pub.slug,
                                      title=pub.title, url=url)

    # def get_publication_by_id

    def get_last_publications(self, lang, published, page_size):
        if not lang or not isinstance(lang, portal_objs.Language):
            raise ValueError("Language[{}] is not set or not a portal.objects.Language".format(lang))

        pager = models.Publication.objects.pager_and_last_pubs(page_size, lang_code=lang.code,
                                                               published=published)
        return pager.replace_page(tuple(self._publication_preview(p) for p in pager.page))

    # def get_last_publications

    def _publication_preview(self, pub):
        if not pub or not isinstance(pub, models.Publication):
            raise ValueError("Publication[{}] is not set or not a portal.models.Publication".format(pub))

        if pub.rss_url and pub.rss_stream:
            url=pub.rss_url
            custom_link_name = pub.rss_stream.link_caption
        else:
            url = self.urls_resolver.get_publication_url(language_code=pub.locale.lower_code,
                                                         publication_id=pub.id,
                                                         publication_date=pub.publication_date,
                                                         slug=pub.slug)
            custom_link_name = None

        return objects.PublicationPreview(url=url, publication_id=pub.id, title=pub.title or '',
                                          custom_link_name=custom_link_name,
                                          short_text=pub.short_text, published=self._is_published(pub),
                                          publication_date=pub.publication_date,
                                          show_date=pub.show_date)
    # def _publication_preview

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

# class PublicationService
