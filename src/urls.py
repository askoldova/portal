from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
import filebrowser.urls
import tinymce.urls
from portal import views as portal
import publications.views

urlpatterns = (
    url(r'^admin/', include(admin.site.urls)),

    url(r'^admin/filebrowser/', include(filebrowser.urls)),
    url(r'^tinymce/', include(tinymce.urls)),

    url(r'^/?$', portal.index),
    url(r'^(?P<lang>\w\w)/?$', portal.default),
    url(r'^(?P<lang>\w\w)/item,(?P<id>\d+).*/?$', publications.views.old_item),
    url(r'^(?P<lang>\w\w)/(?P<year>\d\d\d\d)/(?P<month>\d\d)/(?P<day>\d\d)/(?P<slug>.+)\.html/?$',
        publications.views.item, name='pubs_publication'),
)

if settings.DEBUG or settings.ENABLE_MEDIA:
    urlpatterns += (
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
            serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

