from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string

from portal.views import path_of, portal_service, generate_redirect_to_url
from portal import objects as portal_objs
from utils import parse_number_or_http_404, pages_range
from . import STATUS_PUBLISHED, objects, services
import generation as gen

__author__ = 'andriy'


def lang_of(code):
    lang = portal_service.get_language(code)
    if lang == portal_objs.Language.LANGUAGE_NOT_FOUND:
        raise Http404("Language %s is not found" % (code,))
    if lang.code.lower() != code:
        raise Http404("Language %s is not found" % (code,))
    return lang

# === begin of old_url_view

def old_item_view(request, lang, id):
    return HttpResponse(generate_old_item(path_of(request), lang, id).content)

old_item_view_admin = login_required(old_item_view)


def generate_old_item(original_url, lang, old_id):
    old_id = parse_number_or_http_404(old_id, "id {} is not a number".format(old_id))
    lang = lang_of(code=lang)
    item = portal_service.get_publication_ref_by_old_id(id=old_id, lang=lang)
    if item == objects.PUBLICATION_NOT_FOUND or not item.id:
        raise Http404("Publication oldId={} lang={} is not found".format(old_id), lang)
    if item.state != STATUS_PUBLISHED:
        raise Http404("Publication oldId={} lang={} is not published".format(old_id, lang))
    return generate_redirect_to_url(original_url, item, url_of_publication(item))

def url_of_publication(item):
    pass

def old_ulr_of_publication(lang_code, old_id):
    return urlresolvers.reverse(old_item_view, kwargs=dict(lang=lang_code, id=str(old_id)))

# === end of old_url_view

class Resolver(services.UrlsResolver):
    def __init__(self):
        services.UrlsResolver.__init__(self)

    # def __init__

    def get_publication_url(self, language_code, publication_id, publication_date, slug):
        return ulr_of_publication(lang=language_code, publication_date=publication_date,
                                  publication_id=publication_id, slug=slug)

    # def get_publication_url

    def get_old_publication_url(self, lang_code, old_id):
        return old_ulr_of_publication(lang_code=lang_code, old_id=old_id)

    # def get_old_publication_url
# class Resolver

resolver = Resolver()
publications_service = services.PublicationService(resolver, portal_service=portal_service)


# === begin of all publications views ===

def all_publications_view(request, lang):
    return HttpResponse(generate_all_publications(path_of(request), lang).content)

all_publications_view_admin = login_required(all_publications_view)

def all_publications_page_view(request, lang, page):
    return HttpResponse(generate_all_publications_page(path_of(request), lang).content)

all_publications_page_view_admin = login_required(all_publications_page_view)

# --- urls all_publications
def url_of_all_publications(language_code):
    return urlresolvers.reverse(all_publications_view, kwargs=dict(lang=language_code))

def url_of_all_publications_page(language_code, page):
    return urlresolvers.reverse(all_publications_page_view, kwargs=dict(lang=language_code, page=page))

# --- generate all_publications

def generate_all_publications(url, lang):
    lang = lang_of(lang)
    pager = publications_service.get_last_publications(lang, False, 10)

    return gen.GenerationResult(
        url=url,
        content=render_to_string("publications.html", context=dict(
            langs=portal_service.get_languages(lang),
            lang=lang,
            page_nr=pager.page_nr,
            pages=pager.pages,
            page=pager.page,
            navigate_url=url_of_all_publications_page(lang.lower_code, 999999),
            pages_range=pages_range(pager.pages, pager.page, url_of_all_publications_page,
                                    language_code=lang.lower_code)
        ))
    )

def generate_all_publications_page(param, lang):
    pass


# === end of all publications views ===

# === begin of publication views ===

def ulr_of_publication(lang, publication_date, publication_id, slug):
    """
    :type lang: basestring
    :type publication_date: datetime.date
    :type publication_id: long
    :type slug: basestring
    :rtype: basestr
    """
    slug = slug or str(publication_id)
    year, month, day = "{:04}".format(publication_date.year), "{:02}".format(publication_date.month),\
                       "{:02}".format(publication_date.day)
    return urlresolvers.reverse(publication_view, kwargs=dict(lang=lang, year=year, month=month, day=day, slug=slug))
# def url_of_publication

def publication_view(request, lang, year, month, day, slug):
    return None

publication_view_admin = login_required(publication_view)

# === end of publications view ===
