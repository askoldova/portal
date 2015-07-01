import collections
import datetime

__author__ = 'andriyg'

class FormattedDate(collections.namedtuple("FormattedDate", "year month day")):
    def __new__(cls, date):
        """
        :type date: datetime.date
        """
        if not date and not (isinstance(date, datetime.date) or isinstance(date, datetime.datetime)):
            raise ValueError("date [] is not a date or datetime".format(date))
        return super(FormattedDate, cls).__new__(cls, year="{:04}".format(date.year),
                                                 month="{:02}".format(date.month),
                                                 day="{:02}".format(date.day))
    # def __new__

# class FormattedDate

def dict_of_publication_url_parts(lang, publication_date, publication_id, slug):
    """
    :type lang: basestring
    :type publication_date: datetime.date
    :param publication_id: long
    :param slug: str
    :return: dict
    """
    date = FormattedDate(publication_date)
    return dict(
        lang=lang,
        year=date.year,
        month=date.month,
        day=date.day,
        slug=str(slug or publication_id)
    )
# dict_of_publication_url_parts

