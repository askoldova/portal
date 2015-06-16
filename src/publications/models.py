from django.contrib.auth.models import User

__author__ = 'andriy'

from django.db import models
from tinymce import models as tinymce
from portal import models as portal
from . import *


class PublicationManager(models.Manager):
    pass


class Publication(models.Model):
    type = models.CharField(max_length=20, choices=TYPES.items(), default=TYPE_PUBLICATION)
    slug = models.CharField(max_length=100, unique=True)
    rss_stream = models.IntegerField()
    rss_url = models.CharField(max_length=255)

    objects = PublicationManager()

    class Meta:
        unique_together = (("rss_stream", "rss_url"), )
# class Publication


class PublicationItemManager(models.Manager):
    pass


class PublicationItem(models.Model):
    publication_date = models.DateTimeField(auto_now_add=True)
    show_date = models.BooleanField(default=False)
    locale = models.ForeignKey(to=portal.Lang)
    state = models.CharField(max_length=5, choices=STATUSES.items(), default=STATUS_DRAFT)
    title = models.CharField(max_length=100)
    short_text = tinymce.HTMLField()
    text = tinymce.HTMLField()
    publication = models.ForeignKey(to=Publication)
    author = models.ForeignKey(to=User)

    objects = PublicationItemManager()


class PublicationSubcategoryManager(models.Manager):
    pass


class PublicationSubcategory(models.Model):
    publication = models.ForeignKey(to=Publication)
    subcategory = models.ForeignKey(to=portal.MenuItem)

    objects = PublicationSubcategoryManager()

