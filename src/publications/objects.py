import collections
from portal import objects as portal
from publications import STATUS_DRAFT
import utils

__author__ = 'andriy'

class Ref(collections.namedtuple("Ref", "url title id")):
    def __new__(cls, url, title, id=None):
        return super(Ref, cls).__new__(cls, url=url, title=title, id=id)

    # def __new__

# class Ref


class PublicationRef(collections.namedtuple("PublicationRef",
                                            "publication_id old_id language slug "
                                            "publication_date title url status")):
    def __new__(cls, publication_id, language, title, publication_date, url, slug, status, old_id=None):
        """
        :type publication_id: long
        :type language: portal.objects.Language
        :type title: basestring
        :type publication_date: datetime.date
        :type url: basestring
        :type slug: basestring
        :type status: basestring
        :type old_id: long
        """
        return super(PublicationRef, cls).__new__(cls, publication_id=publication_id,
                                                  language=language,
                                                  title=title, publication_date=publication_date,
                                                  old_id=old_id, url=url, slug=slug, status=status)
    # def __new__

# class publication_ref

PUB_REF_NOT_FOUND = PublicationRef(publication_id=0, slug='', url='', title='',
                                   publication_date=utils.MIN_DATE,
                                   language=portal.LANGUAGE_NOT_FOUND, status=STATUS_DRAFT)


class Pager(collections.namedtuple("Pager", "page_nr pages page")):
    def replace_page(self, new_page):
        return self._replace(page=new_page)
    # def replace_page
# class Pager

PAGE_NOT_FOUND = Pager(0, 0, ())


class PublicationPreview(collections.namedtuple("PublicationPreview",
                                                "url publication_id title "
                                                "custom_link_name short_text published "
                                                "publication_date show_date")):
    pass
# class PublicationPreview


class PublicationView(collections.namedtuple("PublicationView",
                                             "pub_date show_date title text "
                                             "categories imagesi url")):
    def __new__(cls, pub_date, show_date, title, text, categories, images, url):
        return super(PublicationView, cls).\
            __new__(cls, pub_date=pub_date, show_date=show_date, title=title,
                    text=text, categories=categories, images=images, url)

    # def __new__

# class PublicationView


PUB_NOT_FOUND = PublicationView(pub_date=utils.MIN_DATE, show_date=False,
                                title='', text='No text', categories=(), images=())
