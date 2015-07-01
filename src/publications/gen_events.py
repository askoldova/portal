from portal.gen_events import *
from . import check_exist_and_type

__author__ = 'andriyg'


class PublicationGenerate(collections.namedtuple("PublicationPageGenerate", "publication_id")):
    def __new__(cls, publication_id):
        check_exist_and_type(publication_id, "publication_id", int, long)
        return super(PublicationGenerate, cls).__new__(cls, publication_id=publication_id)

# class PublicationGenerate

class OldPublicationGenerate(collections.namedtuple("PublicationPageGenerate", "old_id lang_code")):
    def __new__(cls, old_id, lang_code):
        check_exist_and_type(old_id, "old_id", int, long)
        check_exist_and_type(lang_code, "lang_code", basestring)
        return super(OldPublicationGenerate, cls).__new__(cls, old_id=old_id, lang_code=lang_code)

# class PublicationPageGenerate
