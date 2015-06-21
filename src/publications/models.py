from django.contrib.auth.models import User

__author__ = 'andriy'

from django.db import models
from tinymce import models as tinymce
from filebrowser import fields as filebrowser
from portal import models as portal
from . import *

class RssImportStreams(models.Manager):
    enabled = models.BooleanField(default=True)
    rss_url = models.CharField(max_length=256)
    pool_period_mins = models.IntegerField(default=30)
    language = models.ForeignKey(to=portal.Lang)
    link_caption = models.CharField(max_length=255)
    menu_item = models.ForeignKey(to=portal.MenuItem)


class PublicationManager(models.Manager):
    pass


class Publication(models.Model):
    type = models.CharField(max_length=20, choices=TYPES.items(), default=TYPE_PUBLICATION)
    slug = models.CharField(max_length=100, unique=True, null=True, blank=True)
    rss_stream = models.IntegerField(null=True, blank=True)
    rss_url = models.CharField(max_length=255, null=True, blank=True)
    subcategory = models.ForeignKey(to=portal.MenuItem)

    objects = PublicationManager()

    class Meta:
        unique_together = (("rss_stream", "rss_url"), )
# class Publication


class PublicationItemManager(models.Manager):
    pass


class PublicationItem(models.Model):
    publication_date = models.DateTimeField()
    show_date = models.BooleanField(default=False)
    locale = models.ForeignKey(to=portal.Lang)
    state = models.CharField(max_length=5, choices=STATUSES.items(), default=STATUS_DRAFT)
    title = models.CharField(max_length=256, blank=True, null=True)
    short_text = tinymce.HTMLField()
    text = tinymce.HTMLField(blank=True, null=True)
    publication = models.ForeignKey(to=Publication)
    author = models.ForeignKey(to=User, null=True, blank=True)

    objects = PublicationItemManager()


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

