from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
from django.http import HttpResponse
from portal.views import path_of, lang_of, portal_service, generate_concrete_redirect
from utils import parse_number_or_http_404
from . import services

__author__ = 'andriy'


def old_item(request, lang, id):
    return HttpResponse(generate_old_item(path_of(request), lang, id).content)


def item(request, lang, year, month, day, slug):
    return None

item_admin = login_required(item)

def generate_old_item(original_url, lang, id):
    id = parse_number_or_http_404(id, "id %s is not a number" % (id,))
    lang = lang_of(code=lang)
    item = portal_service.get_publication_item_by_id(id=id, lang=lang)
    return generate_concrete_redirect(original_url, item, (), year=0, month=0, day=0, slug='')


def old_item_ulr(lang_code, id):
    if not lang_code or not isinstance(lang_code, basestring):
        raise ValueError("lang_code [%s] have to be a sting" % (lang_code,))
    if not id or not (isinstance(id, long) or isinstance(id, int)):
        raise ValueError("id [%s] have to be a int" % (id,))

    return urlresolvers.reverse(old_item, kwargs=dict(lang=lang_code, id=str(id)))


publications_service = services.PublicationService()



