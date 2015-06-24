import collections
from portal import objects as portal
import utils

__author__ = 'andriy'

class Ref(collections.namedtuple("Ref", "url title id")):
    def __new__(cls, url, title, id=None):
        return super(Ref, cls).__new__(cls, url=url, title=title, id=id)

    # def __new__

# class Ref


class PublicationRef(collections.namedtuple("PublicationRef",
                                            "publication_id old_id language_code slug "
                                            "publication_date title url")):
    def __new__(cls, publication_id, language_code, title, publication_date, url, slug, old_id=None):
        return super(PublicationRef, cls).__new__(cls, publication_id=publication_id,
                                                  language_code=language_code,
                                                  title=title, publication_date=publication_date,
                                                  old_id=old_id, url=url, slug=slug)
    # def __new__

# class publication_ref

PUBLICATION_NOT_FOUND = PublicationRef(publication_id=0, slug='', url='', title='',
                                            publication_date=utils.MIN_DATE,
                                            language_code=portal.LANGUAGE_NOT_FOUND.code.lower())


class Pager(collections.namedtuple("Pager", "page_nr pages page")):
    def replace_page(self, new_page):
        return self._replace(page=new_page)
    # def replace_page
# class Pager

class PublicationPreview(collections.namedtuple("PublicationPreview",
                                                "url publication_id title "
                                                "custom_link_name short_text published "
                                                "publication_date show_date")):
    pass
# class PublicationPreview
