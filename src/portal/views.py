import types

from django.core import urlresolvers
from django.http import HttpResponse, Http404
from django.template import loader, Context

from . import service
import generation as gen
from portal import objects

portal_service = service.PortalService()
publication_service = service.PublicationsService(portal_service=portal_service)

def path_of(request):
    return request.META['PATH_INFO'] if 'PATH_INFO' in request.META else ''

def generate_concrete_redirect(original_url, view_to, view_args, view_kwargs):
    url = urlresolvers.reverse(viewname=view_to, args=view_args, kwargs=view_kwargs)
    string = loader.render_to_string("redirect.html",
                                     context=Context(dict(location=url)))
    return gen.GenerationResult(original_url, string)


def generate_redirect_to(original_url, args_to, kwargs, kwargs_to, view_to):
    kwargs = dict((k, v if not isinstance(v, types.FunctionType) else v()) for k, v in kwargs.items())
    view_args = tuple([kwargs[k] if k else None for k in args_to])
    view_kwargs = dict((k, v) for k, v in kwargs.items() if k in kwargs_to)
    return generate_concrete_redirect(original_url, view_to, view_args, view_kwargs)


def redirect_to(request, view_to, args_to=(), kwargs_to=(), **kwargs):
    return HttpResponse(request.META['PATH_INFO'],
                        generate_redirect_to(args_to, kwargs, kwargs_to, view_to).index())



def generate_index(url):
    lang = portal_service.get_default_language()
    if lang == objects.Language.LANGUAGE_NOT_FOUND:
        raise Http404("Default language is not found")
    return generate_concrete_redirect(url, default, view_args=(),
                                      view_kwargs=dict(lang=lang.code.lower()))

def index(url):
    return HttpResponse(generate_index(url).content)

def index_url():
    return urlresolvers.reverse(index)

def generate_default(url, lang_code):
    lang = lang_of(lang_code)
    text = loader.render_to_string("design.html", context=Context(dict(language=lang)))
    return gen.GenerationResult(url, text)


def lang_of(code):
    lang = portal_service.get_language(code)
    if lang == objects.Language.LANGUAGE_NOT_FOUND:
        raise Http404("Language %s is not found" % (code,))
    if lang.code.lower() != code:
        raise Http404("Language %s is not found" % (code,))
    return lang


def default(request, lang):
    return HttpResponse(generate_default(path_of(request), lang).content)


def default_url(language_code):
    return urlresolvers.reverse(default, kwargs=dict(lang=language_code))



