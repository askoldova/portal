import collections
import datetime

__author__ = 'andriyg'

class FormattedDate(collections.namedtuple("FormattedDate", "year month day")):
    def __new__(cls, date):
        if not date and not (isinstance(date, datetime.date) or isinstance(date, datetime.date)):
            raise ValueError("date [] is not a date or datetime".format(date))
        return super(FormattedDate, cls).__new__(cls, year="{:04}".format(date.year),
                                                 month="{:02}".format(date.month),
                                                 day="{:02}".format(date.day))
    # def __new__

# class FormattedDate
