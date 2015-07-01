import collections
import datetime
from django.utils.translation import gettext_lazy as _

__author__ = 'andriy'

STATUS_PUBLISHED = 'P'
STATUS_HOLDED = 'H'
STATUS_DRAFT = 'N'
STATUS_HIDDEN = 'I'

STATUSES = {
    STATUS_DRAFT: _("Draft"),
    STATUS_PUBLISHED: _("Published"),
    STATUS_HOLDED: _("Holded"),
    STATUS_HIDDEN: _("Hidden"),
}

TYPE_PUBLICATION = 'Note'
TYPE_RSS = 'Rss'
TYPE_PHOTOGALLERY = 'Photo'

TYPES = {
    TYPE_PUBLICATION: _("Publication"),
    TYPE_RSS: _("Rss"),
    TYPE_PHOTOGALLERY: _("Photogallery"),
}
MIN_DATE = datetime.date(1970, 1, 1)


class Pager(collections.namedtuple("Pager", "page_nr pages page")):
    def replace_page(self, new_page):
        return self._replace(page=new_page)

    # def replace_page


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