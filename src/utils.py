from django.http import Http404


def parse_number_or_http_404(id, error):
    try:
        return long(id)
    except ValueError:
        raise Http404(error)

# def parse_number_or_http_404
