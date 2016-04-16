from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
import filebrowser.urls
import tinymce.urls
from portal import views as portal
from publications import views as pubs

PREVIEW = 'admin/preview/'

publication_url = r'^{}(?P<lang>\w\w)/(?P<year>\d\d\d\d)/(?P<month>\d\d)/(?P<day>\d\d)/(?P<slug>.+)\.html/?$'
index_url = r'^{}$'
all_publications_url = r'^{}(?P<lang>\w\w)/?$'
all_publications_page_url = r'^{}(?P<lang>\w\w)/(?P<page>\d+).html$'
all_old_publications_url = r'^{}(?P<lang>\w\w)/index$'
all_old_publications_page_url = r'^{}(?P<lang>\w\w)/index,(?P<page>\d+)$'
old_publication_url = r'{}^(?P<lang>\w\w)/item,(?P<old_id>\d+).*/?$'

urlpatterns = [
    url(r'^admin/filebrowser/', include(filebrowser.urls)),
    url(r'^admin/tinymce/', include(tinymce.urls)),

    url(r'^admin/', include(admin.site.urls)),

    url(index_url.format(PREVIEW), portal.index_view_admin, name='portal_index_preview'),
    url(all_publications_url.format(PREVIEW),
        pubs.all_publications_view_admin),
    url(all_publications_url.format(PREVIEW),
        pubs.all_publications_view_admin, name='pubs_all_publications_preview'),
    url(all_publications_page_url.format(PREVIEW),
        pubs.all_publications_page_view_admin, name='pubs_all_publications_page_preview'),
    url(all_old_publications_url.format(PREVIEW),
        pubs.all_old_publications_view_admin, name='pubs_all_old_publications_preview'),
    url(all_old_publications_page_url.format(PREVIEW),
        pubs.all_old_publications_page_view_admin, name='pubs_all_old_publications_page_preview'),
    url(all_publications_page_url.format(PREVIEW),
        pubs.all_old_publications_page_view_admin, name='pubs_all_publications_page_preview'),
    url(pubs.menu_item_url.format(PREVIEW), pubs.menu_item_view_admin),
    url(pubs.menu_item_page_url.format(PREVIEW), pubs.menu_item_view_page_admin),
    url(pubs.menu_item_url2.format(PREVIEW), pubs.menu_item_view_admin),
    url(pubs.menu_item_page_url2.format(PREVIEW), pubs.menu_item_view_page_admin),
    url(publication_url.format(PREVIEW), pubs.publication_view_admin, name='pubs_publication_preview'),
]

if (settings.DEBUG or settings.ENABLE_MEDIA) and not settings.FORCE_DISABLE_MEDIA:
    urlpatterns += [
        url(r'^{}(?P<path>.*)$'.format(settings.MEDIA_URL[1:]),
            serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    ]


urlpatterns += [
    url(index_url.format(''), portal.index_view),
    url(all_publications_url.format(''), pubs.all_publications_view, name='pubs_all_publications'),
    url(all_publications_page_url.format(''), pubs.all_publications_page_view),
    url(old_publication_url.format(''), pubs.old_publication_view),
    url(all_old_publications_url.format(''), pubs.all_old_publications_view,
        name='pubs_all_old_publications'),
    url(all_old_publications_page_url.format(''), pubs.all_old_publications_page_view,
        name='pubs_all_old_publications_page'),
    url(pubs.menu_item_url.format(''), pubs.menu_item_view),
    url(pubs.menu_item_page_url.format(''), pubs.menu_item_view_page),
    url(pubs.menu_item_url2.format(''), pubs.menu_item_view),
    url(pubs.menu_item_page_url2.format(''), pubs.menu_item_view_page),
    url(publication_url.format(''), pubs.publication_view),
]
