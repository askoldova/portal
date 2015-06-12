from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
from portal import views as portal


urlpatterns = (
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/?$', portal.index),
    url(r'^(?P<lang>\w\w)/?$', portal.default),
)

if settings.DEBUG or settings.ENABLE_MEDIA:
    urlpatterns += (
        url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
            serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

