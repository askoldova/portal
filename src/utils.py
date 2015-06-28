import datetime
from django.http import Http404


def parse_number_or_http_404(value, error=None):
    try:
        return long(value)
    except ValueError:
        error = error or "Can't parse numeric value [{}]".format(value)
        raise Http404(error)

# def parse_number_or_http_404

MIN_DATE = datetime.date(1970, 1, 1)


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
    range_from = max(2, page-5)
    range_to = min(page+5, pages-1)
    for i in range(range_from, range_to+1):
        plist += _page_and_ref(i),
    if page + 5 < pages - 1:
        plist += (_NONE_REF,)
    plist += _page_and_ref(pages),

    return tuple(reversed(plist))
# def pages_range

def check_exist_and_type(value, name, _type, *types):
    types = types or ()
    if None != _type:
        types = (_type,) + types

    if not value:
        raise ValueError("{} value is not set".format(name))
    if not types:
        return
    for t in types:
        if isinstance(value, t):
            return
    raise ValueError("{} value [{}] is not one of {}".format(name, value, types))

# def check_exists_and_type
