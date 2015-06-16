from django.utils.translation import gettext_lazy as _

__author__ = 'andriy'

STATUS_PUBLISHED = 'P'
STATUS_HOLDED = 'H'
STATUS_DRAFT = 'N'

STATUSES = {
    STATUS_DRAFT: _("Draft"),
    STATUS_PUBLISHED: _("Published"),
    STATUS_HOLDED: _("Holded"),
}

TYPE_PUBLICATION = 'Note'
TYPE_RSS = 'Rss'
TYPE_PHOTOGALLERY = 'Photo'

TYPES = {
    TYPE_PUBLICATION: _("Publication"),
    TYPE_RSS: _("Rss"),
    TYPE_PHOTOGALLERY: _("Photogallery"),
}
