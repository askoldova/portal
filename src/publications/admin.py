from django.contrib import admin
from . import models

__author__ = 'andriy'


class PublicationItemAdmin(admin.StackedInline):
    model = models.PublicationItem
    extra = 1

class PublicationSubcategoryAdmin(admin.TabularInline):
    model = models.PublicationSubcategory
    extra = 1

class PublicationAdmin(admin.ModelAdmin):
    inlines = (PublicationSubcategoryAdmin, PublicationItemAdmin,)


admin.site.register(models.Publication, PublicationAdmin)
