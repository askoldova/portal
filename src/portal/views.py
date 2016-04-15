import types

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
from django.http import HttpResponse, Http404
from django.template import loader, Context

import generation as gen
from portal import objects
from . import services

portal_service = services.PortalService()


def path_of(request):
    return request.META['PATH_INFO'] if 'PATH_INFO' in request.META else ''


def generate_redirect_to_url(original_url, url):
    timeout = settings.REDIRECT_HTML_TIMEOUT
    string = loader.render_to_string("redirect.html",
                                     context=Context(dict(location=url, timeout=timeout)))
    return gen.GenerationResult(original_url, string)


def generate_concrete_redirect(original_url, view_to, view_args=None, view_kwargs=None):
    url = urlresolvers.reverse(viewname=view_to, args=view_args or (), kwargs=view_kwargs or {})
    return generate_redirect_to_url(original_url, url)


def generate_redirect_to(original_url, view_to, args_to=(), kwargs_to=(), **kwargs):
    kwargs = dict((k, v if not isinstance(v, types.FunctionType) else v()) for k, v in kwargs.items())
    view_args = tuple([kwargs[k] if k else None for k in args_to])
    view_kwargs = dict((k, v) for k, v in kwargs.items() if k in kwargs_to)
    return generate_concrete_redirect(original_url, view_to, view_args, view_kwargs)


def redirect_to(request, view_to, args_to=(), kwargs_to=(), **kwargs):
    return HttpResponse(request.META['PATH_INFO'],
                        generate_redirect_to(args_to, kwargs, view_to).index())


def generate_index(url):
    lang = portal_service.get_default_language()
    if lang == objects.Language.LANGUAGE_NOT_FOUND:
        raise Http404("Default language is not found")
    return generate_concrete_redirect(url, settings.PORTAL_DEFAULT_REDIRECT_VIEW, view_args=(),
                                      view_kwargs=dict(lang=lang.code.lower()))


def index_view(url):
    return HttpResponse(generate_index(url).content)


index_view_admin = login_required(index_view)


def index_url():
    return urlresolvers.reverse(index_view)

# def index_url

# === end of index view
