from django.contrib import admin
from . import models
from django.core import urlresolvers

__author__ = 'andriy'


class PublicationItemAdmin(admin.StackedInline):
    model = models.PublicationItem
    extra = 1

    def get_view_on_site_url(self, obj=None):
        """
        :type obj: publications.models.PublicationItem
        :rtype: basestring
        """
        if obj:
            year = "%04d" % (obj.publication_date.year,)
            month = "%02d" % (obj.publication_date.month,)
            day = "%02d" % (obj.publication_date.day,)
            slug = obj.publication.slug or str(obj.publication.id)
            return urlresolvers.reverse('pubs_publication',
                                        kwargs=dict(lang=obj.locale.code.lower(), year=year, month=month, day=day,
                                                    slug=slug))
        return None

# class PublicationItemAdmin


class PublicationSubcategoryAdmin(admin.TabularInline):
    model = models.PublicationSubcategory
    extra = 1

class PublicationAdmin(admin.ModelAdmin):
    inlines = (PublicationSubcategoryAdmin, PublicationItemAdmin,)


admin.site.register(models.Publication, PublicationAdmin)
