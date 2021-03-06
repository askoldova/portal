import collections

import core
from portal import objects as portal
from . import STATUS_DRAFT, Pager, MIN_DATE

__author__ = 'andriy'


class Ref(collections.namedtuple("Ref", "url title id")):
    def __new__(cls, url, title, _id=None):
        return super(Ref, cls).__new__(cls, url=url, title=title, id=_id)

        # def __new__


# class Ref


class PublicationRef(collections.namedtuple("PublicationRef",
                                            "publication_id old_id language slug "
                                            "publication_date title url status categories")):
    def __new__(cls, publication_id, language, title, publication_date, url, slug, status, old_id=None, categories=None):
        """
        :type publication_id: long
        :type language: portal.objects.Language
        :type title: basestring
        :type publication_date: datetime.date
        :type url: basestring
        :type slug: basestring
        :type status: basestring
        :type old_id: long
        :type categories: list[publication.objects.SubcategoryRefs]
        """
        return super(PublicationRef, cls).__new__(cls, publication_id=publication_id,
                                                  language=language,
                                                  title=title, publication_date=publication_date,
                                                  old_id=old_id, url=url, slug=slug, status=status,
                                                  categories=categories or [])
        # def __new__


# class publication_ref

PUB_REF_NOT_FOUND = PublicationRef(publication_id=0, slug='', url='', title='',
                                   publication_date=MIN_DATE,
                                   language=portal.LANGUAGE_NOT_FOUND, status=STATUS_DRAFT)

PAGE_NOT_FOUND = Pager(0, 0, ())


class PublicationPreview(collections.namedtuple("PublicationPreview",
                                                "url publication_id title "
                                                "custom_link_name short_text published "
                                                "publication_date show_date categories")):
    def __new__(cls, *args, **kwargs):
        return super(PublicationPreview, cls).__new__(cls, *args, **kwargs)


# class PublicationPreview


class PublicationView(collections.namedtuple("PublicationView",
                                             "lang url title pub_date show_date text "
                                             "categories images")):
    def __new__(cls, lang, pub_date, show_date, title, text, categories, images, url):
        return super(PublicationView, cls). \
            __new__(cls, lang=lang, pub_date=pub_date, show_date=show_date, title=title,
                    text=text, categories=categories, images=images, url=url)

        # def __new__


# class PublicationView


PUB_NOT_FOUND = PublicationView(lang=portal.LANGUAGE_NOT_FOUND, pub_date=MIN_DATE, show_date=False, url='',
                                title='', text='No text', categories=(), images=())


class SubcategoryRef(collections.namedtuple("SubcategoryRef", "code title lang url slug")):
    def __new__(cls, code, title, lang, url, slug):
        core.check_exist_and_type(code, "code", int, long)
        core.check_exist_and_type(title, "title", str, unicode)
        core.check_exist_and_type(lang, "lang", portal.Language)
        core.check_exist_and_type(url, "url", str, unicode)
        core.check_type(slug, "slug", str, unicode)
        return super(SubcategoryRef, cls).__new__(cls, code=code, title=title, lang=lang, url=url, slug=slug)


class CategoryRef(collections.namedtuple("CategoryRef", "code title width items")):
    def __new__(cls, code, title, width, items):
        core.check_int_value(code=code)
        core.check_string_value(title=title)
        core.check_type2(tuple, items=items)
        core.check_int(width=width)
        return super(CategoryRef, cls).__new__(cls, code=code, title=title, width=width, items=items)


class RegionItem(collections.namedtuple("RegionItem", "title url body")):
    def __new__(cls, title, url, body):
        core.check_string(title=title)
        core.check_string(url=url)
        core.check_string(body=body)
        return super(RegionItem, cls).__new__(cls, title, url, body)