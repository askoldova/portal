from django.conf.urls import patterns, url
from django.contrib import admin
from django.http import HttpResponseRedirect
from . import models

class GenerationAdmin(admin.ModelAdmin):
    actions = []

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        # noinspection PyProtectedMember
        opts = self.model._meta
        info = opts.app_label, (opts.model_name if hasattr(opts, 'model_name') else opts.module_name)
        return patterns('',
            url('^$', self.admin_site.admin_view(self.view), name='{0}_{1}_changelist'.format(*info)),
        )

    def view(self, request):
        return HttpResponseRedirect('/')


admin.site.register(models.Generation, GenerationAdmin)
