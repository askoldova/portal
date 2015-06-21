from django.contrib import admin
from . import models
from django.core import urlresolvers

__author__ = 'andriy'


class PublicationItemAdmin(admin.ModelAdmin):
    model = models.Publication
    extra = 1

    def get_view_on_site_url(self, obj=None):
        """
        :type obj: publications.models.Publication
        :rtype: basestring
        """
        if obj:
            year = "%04d" % (obj.publication_date.year,)
            month = "%02d" % (obj.publication_date.month + 1,)
            day = "%02d" % (obj.publication_date.day,)
            slug = obj.publication.slug or str(obj.publication.id)
            return urlresolvers.reverse('pubs_publication',
                                        kwargs=dict(lang=obj.locale.code.lower(), year=year, month=month, day=day,
                                                    slug=slug))
        return None

    readonly_fields = ("old_id",)
# class PublicationItemAdmin


class PublicationSubcategoryAdmin(admin.TabularInline):
    model = models.PublicationSubcategory
    extra = 1


class PublicationImagesAdmin(admin.TabularInline):
    model = models.PublicationImage
    exclude = ('name',)
    extra = 3


class PublicationAdmin(admin.ModelAdmin):
    inlines = (PublicationSubcategoryAdmin, PublicationImagesAdmin,)


admin.site.register(models.Publication, PublicationAdmin)
admin.site.register(models.RssImportStream)
