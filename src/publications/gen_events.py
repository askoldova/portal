import collections

__author__ = 'andriyg'


class PublicationPageGenerate(collections.namedtuple("PublicationPageGenerate", "publication_id")):
    def __new__(cls, publication_id):
        if not publication_id:
            raise ValueError("publication_id is not set")
        return super(PublicationPageGenerate, cls).__new__(cls, publication_id=publication_id)

# class PublicationPageGenerate
