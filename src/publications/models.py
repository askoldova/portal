import datetime

from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

import core
import generation
from . import gen_events

__author__ = 'andriy'

from django.db import models
from tinymce import models as tinymce
from filebrowser import fields as filebrowser
from portal import models as portal
from . import Pager, STATUS_PUBLISHED, STATUSES, TYPES, STATUS_DRAFT, TYPE_PUBLICATION


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

    def __unicode__(self):
        return u"{}".format(self.menu_item.caption)

# enc class RssImportStream


def publication_filter_by_subcategory(menu_item_id, q):
    core.check_exist_and_type2(models.QuerySet, q=q)
    core.check_exist_and_type2(int, long, menu_item_id=menu_item_id)

    q = q.filter(subcategory__id=menu_item_id) | \
        q.filter(publicationsubcategory__subcategory__id=menu_item_id)
    return q


def publication_filter_by_category(main_menu_id, q):
    core.check_exist_and_type2(models.QuerySet, q=q)
    core.check_exist_and_type2(int, long, main_menu_id=main_menu_id)

    q = q.filter(subcategory__menu__id=main_menu_id) | \
        q.filter(publicationsubcategory__subcategory__menu__id=main_menu_id)
    return q


class PublicationManager(models.Manager):
    def get_by_id(self, publication_id):
        """
        :type publication_id: long
        :rtype: publications.models.Publication
        """
        return self.get(id=publication_id)

    # def get_by_id

    def get_by_land_and_old_id(self, lang_code, old_id):
        """
        :type lang_code: str|unicode
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
        return pages or 1, remind

    # def `_count_pages

    def pager_and_last_pubs(self, page_size, lang_code):
        page_size, q = self._fix_page_size_and_get_pub_query(lang_code, page_size)

        pages, remind = self._count_pages(page_size, q)

        return Pager(page_nr=pages, pages=pages, page=tuple(q[:page_size]))

    def pager_and_last_menu_pubs(self, page_size, lang_code, menu_item_id):
        page_size, q = self._fix_page_size_and_get_pub_query(lang_code, page_size)
        q = publication_filter_by_subcategory(menu_item_id, q)

        pages, remind = self._count_pages(page_size, q)

        return Pager(page_nr=pages, pages=pages, page=tuple(q[:page_size]))

    def pager_and_menu_pubs_page(self, page, page_size, lang_code, menu_item_id):
        page_size, q = self._fix_page_size_and_get_pub_query(lang_code, page_size)
        q = publication_filter_by_subcategory(menu_item_id, q)

        return self._get_page_from_query(page, page_size, q)

    # def pager_and_last_pubs

    def pager_and_all_pubs_page(self, page, page_size, lang_code):
        page_size, q = self._fix_page_size_and_get_pub_query(lang_code, page_size)

        return self._get_page_from_query(page, page_size, q)

    def _get_page_from_query(self, page, page_size, q):
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
        return Pager(page_nr=page, pages=pages, page=page_data)

    def _fix_page_size_and_get_pub_query(self, lang_code, page_size):
        if page_size <= 0:
            page_size = 1
        q = self.filter(locale__code=lang_code.upper()).filter(state=STATUS_PUBLISHED)
        return page_size, q

    # def pager_and_all_pubs_page

    def pager_all_pubs(self, lang_code, page_size):
        page_size, q = self._fix_page_size_and_get_pub_query(lang_code, page_size)

        pages, remind = self._count_pages(page_size, q)

        return Pager(page_nr=1, pages=pages, page=())

    # def pager_all_pubs_to

    def get_by_lang_date_slug(self, lang_code, publication_date,
                              publication_id, slug):
        """
        :type lang_code: basestring
        :type publication_date: datetime.date
        :type publication_id: long
        :type slug: str|unicode
        :rtype: publications.models.Publication
        """
        next_pub_date = publication_date + datetime.timedelta(days=1)
        return self.filter(locale__code=lang_code.upper(),
                           publication_date__gte=publication_date,
                           publication_date__lt=next_pub_date). \
            filter(Q(id=publication_id) | Q(slug=slug)).get()

        # def get_by_lang_date_slug


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
    rss_url = models.CharField(max_length=512, null=True, blank=True)
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
        index_together = (("state", "publication_date"), ("state", "subcategory", "publication_date"),)
        ordering = ("-publication_date",)


# class Publication


class PublicationSubcategoryManager(models.Manager):
    def find_by_publication(self, pub):
        return [f.subcategory for f in self.filter(publication__exact=pub)]


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


class PortalRegion(models.Model):
    region_name = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        name = self.region_name
        for i in self.portalregioncontent_set.all():
            name += u"\n{}".format(i.latest_from or i.one_from
                                   or (i.publication.title if i.publication else None) or i.title)
        return name


class PortalRegionContentManager(models.Manager):
    def get_by_region_name(self, region_name):
        core.check_string_value(region_name=region_name)

        return self.filter(region__region_name=region_name)


class PortalRegionContent(models.Model):
    region = models.ForeignKey(to=PortalRegion)
    order = models.IntegerField(default=100)
    latest_from = models.ForeignKey(to=portal.MenuItem, blank=True, null=True, related_name="latest_from_regions")
    one_from = models.ForeignKey(to=portal.MenuItem, blank=True, null=True, related_name="one_from_regions")
    publication = models.ForeignKey(to=Publication, blank=True, null=True)
    title = models.CharField(max_length=256, blank=True, null=True)
    url = models.CharField(max_length=256, blank=True, null=True)
    text = tinymce.HTMLField(blank=True, null=True)

    objects = PortalRegionContentManager()

    class Meta:
        ordering = ("region__region_name", "order", "id", )
