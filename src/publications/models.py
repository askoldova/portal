from django.contrib.auth.models import User
from . import gen_events, objects
from django.utils.translation import gettext_lazy as _
import generation

__author__ = 'andriy'

from django.db import models
from tinymce import models as tinymce
from filebrowser import fields as filebrowser
from portal import models as portal
from . import *


class RssImportStreamManager(models.Manager):
    pass


class RssImportStream(models.Model):
    enabled = models.BooleanField(default=True)
    rss_url = models.CharField(max_length=256)
    pool_period_mins = models.IntegerField(default=30)
    next_pool = models.DateTimeField()
    language = models.ForeignKey(to=portal.Lang)
    link_caption = models.CharField(max_length=255)
    menu_item = models.ForeignKey(to=portal.MenuItem)

    objects = RssImportStreamManager()

# enc class RssImportStream


class PublicationManager(models.Manager):
    def get_by_id(self, publication_id):
        """
        :type publication_id: long
        :rtype: publications.models.Publication
        """
        return self.get(id = publication_id)

    # def get_by_id

    def get_by_land_and_old_id(self, lang_code, old_id):
        """
        :type lang_code: basestring
        :type old_id: long
        :rtype: publications.models.Publication
        """
        return self.get(old_id=old_id, locale__code=lang_code.upper())

    # def get_by_land_and_old_id

    def _count_pages(self, page_size, q):
        at_all = q.aggregate(models.Count('id'))
        pages, remind = divmod(at_all['id__count'], page_size)
        if remind > 0:
            pages += 1
        return pages, remind
    # def `_count_pages

    def pager_and_last_pubs(self, page_size, lang_code):
        page_size, q = self._fix_page_size_and_get_pub_query(lang_code, page_size)

        pages, remind = self._count_pages(page_size, q)

        return objects.Pager(page_nr=pages, pages=pages, page=tuple(q[:page_size]))

    # def pager_and_last_pubs

    def pager_and_all_pubs_page(self, page, page_size, lang_code):
        page_size, q = self._fix_page_size_and_get_pub_query(lang_code, page_size)

        pages, remind = self._count_pages(page_size, q)
        if page > pages:
            page_data = ()
        elif page <= pages / 2:
            page_data = tuple(q.reverse()[(page - 1) * page_size:page * page_size])
            page_data = tuple(reversed(page_data))
        elif remind == 0:
            _from = remind + (pages - page) * page_size
            _to = remind + (pages - page + 1) * page_size

            page_data = tuple(q[_from:_to])
        elif page == pages:
            page_data = tuple(q[0:remind])
        else:
            _from = remind + (pages - page - 1) * page_size
            _to = remind + (pages - page) * page_size

            page_data = tuple(q[_from:_to])

        return objects.Pager(page_nr=page, pages=pages, page=page_data)

    def _fix_page_size_and_get_pub_query(self, lang_code, page_size):
        if page_size <= 0:
            page_size = 1
        q = self.filter(locale__code=lang_code.upper()).filter(state=STATUS_PUBLISHED)
        return page_size, q

    # def pager_and_all_pubs_page

    def pager_all_pubs(self, lang_code, page_size):
        page_size, q = self._fix_page_size_and_get_pub_query(lang_code, page_size)

        pages, remind = self._count_pages(page_size, q)

        return objects.Pager(page_nr=1, pages=pages, page=())

    # def pager_all_pubs_to

# class PublicationManager


class Publication(models.Model):
    state = models.CharField(max_length=5, choices=STATUSES.items(), default=STATUS_DRAFT)
    publication_date = models.DateField(db_index=True)
    show_date = models.BooleanField(default=False)
    slug = models.CharField(max_length=100, null=True, blank=True, unique_for_date="publication_date")
    type = models.CharField(max_length=20, choices=TYPES.items(), default=TYPE_PUBLICATION)
    locale = models.ForeignKey(to=portal.Lang)
    title = models.CharField(max_length=256, blank=True, null=True)
    subcategory = models.ForeignKey(to=portal.MenuItem)
    short_text = tinymce.HTMLField()
    text = tinymce.HTMLField(blank=True, null=True)
    author = models.ForeignKey(to=User, null=True, blank=True)

    rss_stream = models.ForeignKey(to=RssImportStream, null=True, blank=True)
    rss_url = models.CharField(max_length=255, null=True, blank=True)
    old_id = models.IntegerField(null=True, blank=True, db_index=True)

    objects = PublicationManager()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Publication, self).save(force_insert, force_update, using, update_fields)
        generation.apply_generation_task(gen_events.PublicationGenerate(self.id))

    # def save

    def title_int(self):
        return self.title or u"{} {}".format(self.publication_date, self.slug or self.old_id or self.id)

    def __unicode__(self):
        return u"{} ({})".format(self.title_int(), self.locale.code.lower())

    class Meta:
        unique_together = (("rss_stream", "rss_url"), ("publication_date", "slug"),)
        index_together = (("state", "publication_date"),("state", "subcategory", "publication_date"),)
        ordering = ("-publication_date",)

# class Publication


class PublicationSubcategoryManager(models.Manager):
    pass


class PublicationSubcategory(models.Model):
    publication = models.ForeignKey(to=Publication)
    subcategory = models.ForeignKey(to=portal.MenuItem)

    objects = PublicationSubcategoryManager()


class PublicationImageManages(models.Manager):
    pass


class PublicationImage(models.Model):
    publication = models.ForeignKey(to=Publication)
    file = filebrowser.FileBrowseField(max_length=255)
    caption = filebrowser.CharField(max_length=255, null=True, blank=True)
    name = filebrowser.CharField(max_length=128, null=True, blank=True)

    objects = PublicationImageManages()

    class Meta:
        unique_together = (("publication", "file"),)
        ordering = ("id",)
# class PublicationImage


class ConfigurationManager(models.Manager):
    def get_configuration(self):
        """
        :rtype: publications.models.Configuration
        """
        try:
            return self.get()
        except Configuration.DoesNotExist:
            conf = self.create()
            conf.save()
            return conf

    # def get_configuration
# class ConfigurationManager


class Configuration(models.Model):
    publications_page_size = models.IntegerField(default=6, verbose_name=_("News Page Size"))
    last_old_publication = models.ForeignKey(to=Publication, blank=True, null=True)

    objects = ConfigurationManager()

    def __unicode__(self):
        return u"Configuration"
# class Configuration
