import os
from django.conf import settings
from django.test import TestCase
from django.contrib.sites.models import Site
from filebrowser.functions import version_generator
from . import services
from portal.services import PortalService

def fake_reverse(self, view_name, *args, **kwargs):
    return u'/name=%s/args=%s/kwargs%s' % (view_name, args, kwargs)


class ResolverStub(services.UrlsResolver):
    def get_publication_url(self, language_code, publication_id, publication_date, slug):
        """
        :type publication_date: datetime.date

        """
        year = publication_date.year
        month = publication_date.month
        day = publication_date.day
        return "{}/{:04}/{:02}/{:02}/{}.html".format(language_code, year, month, day, slug or str(publication_id))

    def get_old_publication_url(self, lang_code, old_id):
        if not old_id:
            raise ValueError("old_id is not set")
        return "{}/item,{}".format(lang_code, old_id)


resolver = ResolverStub()

pubs_service = services.PublicationService(urls_resolver=resolver, portal_service=PortalService)
pubs_service.portal_service.reverse = fake_reverse


def _setup():
    site = Site.objects.get_current()

    print(site.name, " ", site.domain)

    site.domain = 'test.com'
    site.save()

    site = Site.objects.get_current()
    print(site)

    try:
        site2 = Site.objects.get(name="test2")
    except Site.DoesNotExist:
        site2 = Site()
    site2.name = "test2"
    site2.domain = "https://site2.name/"
    site2.save()

    print(site2.id, " ", site2.name, " ", site2.domain)

    return site, site2
# def _setup


class PublicationsServicesTest(TestCase):
    def __init__(self, method_name='runTest'):
        super(PublicationsServicesTest, self).__init__(method_name)

    def setUp(self):
        super(PublicationsServicesTest, self).setUp()

        self.site, self.site2 = _setup()
    # def __init__

    def test_url(self):
        site2 = self.site2
        site = self.site

    # def test_url

# class CoreServiceTest
