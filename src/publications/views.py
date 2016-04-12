# coding=utf-8

from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string

import core
import generation as gen
import publications
from portal import objects as portal_objs
from portal.views import path_of, portal_service, generate_concrete_redirect
from publications.publication import dict_of_publication_url_parts
from . import STATUS_PUBLISHED, objects, services, STATUS_HIDDEN

__author__ = 'andriy'


def lang_of(code):
    lang = portal_service.get_language(code)
    if lang == portal_objs.Language.LANGUAGE_NOT_FOUND:
        raise Http404("Language %s is not found" % (code,))
    if lang.code.lower() != code:
        raise Http404("Language %s is not found" % (code,))
    return lang


# def lang_of

class Resolver(services.UrlsResolver):
    def __init__(self):
        services.UrlsResolver.__init__(self)

    # def __init__

    def get_publication_url(self, language_code, publication_id, publication_date, slug):
        return url_of_publication(lang=language_code, publication_date=publication_date,
                                  publication_id=publication_id, slug=slug)

    # def get_publication_url

    def get_old_publication_url(self, lang_code, old_id):
        return url_of_old_publication(lang_code=lang_code, old_id=old_id)

        # def get_old_publication_url


# class Resolver

resolver = Resolver()
publications_service = services.PublicationService(resolver, portal_service=portal_service)


# === begin of all publications views ===

def all_old_publications_view(request, lang):
    return HttpResponse(generate_all_old_publications(path_of(request), lang).content)


all_old_publications_view_admin = login_required(all_old_publications_view)


def all_old_publications_page_view(request, lang, page):
    return HttpResponse(generate_all_old_publications_page(path_of(request), lang, page).content)


all_old_publications_page_view_admin = login_required(all_old_publications_page_view)


def all_publications_view(request, lang):
    return HttpResponse(generate_all_publications(path_of(request), lang).content)


all_publications_view_admin = login_required(all_publications_view)


def all_publications_page_view(request, lang, page):
    return HttpResponse(generate_all_publications_page(path_of(request), lang, page).content)


all_publications_page_view_admin = login_required(all_publications_page_view)


# --- urls all_publications
def url_of_all_publications(language_code):
    return urlresolvers.reverse(all_publications_view, kwargs=dict(lang=language_code))


def url_of_all_publications_page(language_code, page):
    return urlresolvers.reverse(all_publications_page_view, kwargs=dict(lang=language_code, page=page))


# --- generate all_publications

def _generate_pubs_page_view(lang, pager, url, title):
    return gen.GenerationResult(
        url=url,
        content=render_to_string("publications.html", context=dict(
            langs=portal_service.get_languages(lang),
            lang=lang,
            page_nr=pager.page_nr,
            pages=pager.pages,
            page=pager.page,
            navigate_url=url_of_all_publications_page(lang.lower_code, 999999),
            pages_range=pages_range(pager.pages, pager.page_nr, url_of_all_publications_page,
                                    language_code=lang.lower_code),
            title=title
        ))
    )


def generate_all_publications(url, lang):
    lang = lang_of(lang)
    pager = publications_service.get_last_publications(lang, False, 6)
    if pager == objects.PAGE_NOT_FOUND:
        raise Http404("Default page is not found")

    return _generate_pubs_page_view(lang, pager, url, u"Події, новини, заходи")


def generate_all_publications_page(url, lang, page):
    lang = lang_of(lang)
    page = parse_number_or_http_404(page)

    pager = publications_service.get_publications_page(lang, page, 6)
    if pager == objects.PAGE_NOT_FOUND:
        raise Http404("Page [{}] is not found".format(page))

    return _generate_pubs_page_view(lang, pager, url, u"Події, новини, заходи")


def generate_all_old_publications(url, lang):
    return generate_concrete_redirect(url, all_publications_view, view_kwargs=dict(lang=lang))


def generate_all_old_publications_page(url, lang, page):
    lang = lang_of(lang)
    page = parse_number_or_http_404(page)

    new_page = publications_service.get_all_pubs_new_page_by_old(lang, page)
    if not new_page:
        raise Http404("Old page [{} {}] is not found".format(lang.code, page))

    return generate_concrete_redirect(url, all_publications_page_view,
                                      view_kwargs=dict(lang=lang.lower_code, page=new_page))


# === end of all publications views ===

# === begin of publication views ===

def url_of_publication(lang, publication_date, publication_id, slug):
    """
    :type lang: basestring
    :type publication_date: datetime.date
    :type publication_id: long
    :type slug: basestring
    :rtype: basestr
    """
    params = dict_of_publication_url_parts(lang=lang, publication_date=publication_date,
                                           publication_id=publication_id, slug=slug)
    return urlresolvers.reverse(publication_view, kwargs=params)


# def url_of_publication


def url_of_old_publication(lang_code, old_id):
    return urlresolvers.reverse(old_publication_view, kwargs=dict(lang=lang_code, old_id=str(old_id)))


def url_of_publication_by_id(publication_id):
    publication = publications_service.get_publication_ref_by_id(publication_id)
    if publication == objects.PUB_REF_NOT_FOUND:
        raise Http404("Publicatoin publication_id [{}] is not found".format(publication_id))
    return url_of_publication(lang=publication.language.lower_code,
                              publication_date=publication.publication_date,
                              publication_id=publication.publication_id, slug=publication.slug)


# def url_of_old_publication

# -- publication generates

def generate_old_publication(url, lang, old_id):
    lang = lang_of(lang)
    old_id = parse_number_or_http_404(old_id,
                                      "Invalid old publication id [{}] value".format(old_id))

    pub_ref = publications_service.get_publication_ref_by_old_id(lang_code=lang.code, old_id=old_id)
    if pub_ref == objects.PUB_REF_NOT_FOUND:
        raise Http404("Publication old_id={}/{} is not found".format(lang.lower_code, old_id))

    if pub_ref.status not in (STATUS_PUBLISHED, STATUS_HIDDEN):
        raise Http404("Publication old_id={}/{} is not to show".format(lang.lower_code, old_id))

    params = dict_of_publication_url_parts(lang=lang.lower_code, publication_date=pub_ref.publication_date,
                                           publication_id=pub_ref.publication_id, slug=pub_ref.slug)
    return generate_concrete_redirect(original_url=url, view_to=publication_view, view_kwargs=params)


# def generate_old_publication

def _render_publication(url, pub):
    """
    :type url: basestring
    :type pub: publications.objects.PublicationView
    :rtype: generation.GenerationResult
    """
    context = dict(publication=pub)
    core.check_exist_and_type(pub, "publication", objects.PublicationView)
    return gen.GenerationResult(url=url,
                                content=render_to_string("publication.html",
                                                         context=context))


# def _render_publication

def generate_publication_by_id(publication_id):
    publication_id = parse_number_or_http_404(publication_id,
                                              "Invalid publication_id [{}] value".format(publication_id))

    publication = publications_service.get_publication_by_id(publication_id)
    return _render_publication(publication.url, publication)


# def generate_publication_by_id


def generate_publication_by_url(url, lang, year, month, day, slug):
    lang = lang_of(lang)
    year = parse_number_or_http_404(year, "Invalid year [{}] value".format(year))
    month = parse_number_or_http_404(month, "Invalid year [{}] value".format(month))
    day = parse_number_or_http_404(day, "Invalid year [{}] value".format(day))

    pub = publications_service.get_publication_view_by_url(lang, year, month, day, slug)
    if pub == objects.PUB_NOT_FOUND:
        raise Http404("Publication is not found")

    return _render_publication(url, pub)


# def generate_publication_by_url

def publication_view(request, lang, year, month, day, slug):
    return HttpResponse(generate_publication_by_url(path_of(request), lang, year, month, day, slug).content)


publication_view_admin = login_required(publication_view)


def old_publication_view(request, lang, old_id):
    return HttpResponse(generate_old_publication(path_of(request), lang=lang, old_id=old_id).content)


old_publication_view_admin = login_required(old_publication_view)


# === end of publications view ===
def parse_number_or_http_404(value, error=None):
    try:
        return long(value)
    except ValueError:
        error = error or "Can't parse numeric value [{}]".format(value)
        raise Http404(error)


def pages_range(pages, page, urlresolver_func, **kwargs):
    """
    Should return list of pages from pages to one, not more than 13-15 elements.
    Have return first page, null value, page-5 up tp page+5 range, null value, last page
    :type pages int
    :type page int
    :rtype list
    """
    if pages <= 0:
        return ()
    elif pages == 1:
        kwargs['page'] = 1
        return (1, urlresolver_func(**kwargs)),
    if page < 1:
        page = 1
    if page > pages:
        page = pages

    def _page_and_ref(_page):
        kwargs['page'] = _page
        return _page, None if _page == page else urlresolver_func(**kwargs)

    _NONE_REF = ("...", None)

    plist = _page_and_ref(1),
    if page - 5 > 2:
        plist += _NONE_REF,
    range_from = max(2, page - 5)
    range_to = min(page + 5, pages - 1)
    for i in range(range_from, range_to + 1):
        plist += _page_and_ref(i),
    if page + 5 < pages - 1:
        plist += (_NONE_REF,)
    plist += _page_and_ref(pages),

    return tuple(reversed(plist))
