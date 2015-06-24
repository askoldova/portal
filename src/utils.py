import datetime
from django.http import Http404


def parse_number_or_http_404(id, error):
    try:
        return long(id)
    except ValueError:
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

    kwargs['page'] = 1
    plist = (1, urlresolver_func(**kwargs)),
    if page - 5 > 2:
        plist += (("...", None),)
    range_from = max(2, page-5)
    range_to = min(page+5, pages-1)
    for i in range(range_from, range_to+1):
        kwargs['page'] = i
        plist += ((i, urlresolver_func(**kwargs)),)
    if page + 5 < pages - 1:
        plist += (("...", None),)
    kwargs['page'] = pages
    plist +=(pages, urlresolver_func(**kwargs)),

    return tuple(reversed(plist))
# def pages_range

