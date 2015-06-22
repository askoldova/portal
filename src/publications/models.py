from django.contrib.auth.models import User
# noinspection PyUnresolvedReferences
from . import gen_events
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
    pass


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
        generation.apply_generation_task(gen_events.PublicationPageGenerate(self.id))

    class Meta:
        unique_together = (("rss_stream", "rss_url"), ("publication_date", "slug"),)
        index_together = (("state", "publication_date"),("state", "subcategory", "publication_date"),)
        ordering = ("-publication_date",)

    def title_int(self):
        return self.title or u"{} {}".format(self.publication_date, self.slug or self.old_id or self.id)

    def __unicode__(self):
        return u"{} ({})".format(self.title_int(), self.locale.code.lower())
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

