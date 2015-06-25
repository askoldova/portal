__author__ = 'andriy'

from django.contrib import admin
from . import models
from django.core import urlresolvers
# noinspection PyUnresolvedReferences
from . import generators, publication

from portal import services as portal_services

portal_service = portal_services.PortalService()

class PublicationSubcategoryAdmin(admin.TabularInline):
    model = models.PublicationSubcategory
    extra = 1


class PublicationImagesAdmin(admin.TabularInline):
    model = models.PublicationImage
    exclude = ('name',)
    extra = 3


class PublicationAdmin(admin.ModelAdmin):
    inlines = (PublicationSubcategoryAdmin, PublicationImagesAdmin,)
    readonly_fields = ("old_id", "rss_stream", "rss_url",)
    list_display = ("publication_date", "__unicode__", "state", "rss_stream")
    list_display_links = list_display
    date_hierarchy = "publication_date"

    list_filter = ("state", "locale","rss_stream",)

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            slug = str(obj.old_id or obj.slug or obj.id)
            portal_service.set_entity_filebrowser_path("images", *(publication.FormattedDate(obj.publication_date) + (slug,)))
        else:
            portal_service.set_entity_filebrowser_path("images")
        return super(PublicationAdmin, self).get_form(request, obj, **kwargs)

    def get_view_on_site_url(self, obj=None):
        """
        :type obj: publications.models.Publication
        :rtype: basestring
        """
        if obj:
            year = "%04d" % (obj.publication_date.year,)
            month = "%02d" % (obj.publication_date.month + 1,)
            day = "%02d" % (obj.publication_date.day,)
            slug = obj.slug or str(obj.old_id) or str(obj.id)
            return urlresolvers.reverse('pubs_publication_preview',
                                        kwargs=dict(lang=obj.locale.code.lower(), year=year, month=month, day=day,
                                                    slug=slug))
        return None
    # get_view_on_site_url

# class PublicationAdmin

admin.site.register(models.Publication, PublicationAdmin)
admin.site.register(models.RssImportStream)
