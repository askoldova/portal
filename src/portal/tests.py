import os
from django.conf import settings
from django.test import TestCase
from django.contrib.sites.models import Site
from filebrowser.functions import version_generator
from .services import PortalService


def fake_reverse(self, view_name, *args, **kwargs):
    return u'/name=%s/args=%s/kwargs%s' % (view_name, args, kwargs)


portal_service = PortalService()
portal_service.reverse = fake_reverse


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


class PortalServiceTest(TestCase):
    def __init__(self, method_name='runTest'):
        super(PortalServiceTest, self).__init__(method_name)

    def setUp(self):
        super(PortalServiceTest, self).setUp()

        self.site, self.site2 = _setup()
    # def __init__

    def test_url(self):
        site2 = self.site2
        site = self.site

        self.assertEqual(portal_service.full_url('/'), "http://test.com/")
        self.assertEqual(portal_service.full_url(''), "http://test.com/")
        self.assertEqual(portal_service.full_url('url'), "http://test.com/url")
        self.assertEqual(portal_service.full_url('/', site_id=site2.id), "https://site2.name/")
        self.assertEqual(portal_service.full_url('', site_id=site2.id), "https://site2.name/")
        self.assertEqual(portal_service.full_url('url', site_id=site2.id), "https://site2.name/url")

    # def test_url

# class CoreServiceTest


class ImagesUrlsTest(TestCase):
    def __init__(self, methodName='runTest'):
        super(ImagesUrlsTest, self).__init__(methodName)

    def setUp(self):
        super(ImagesUrlsTest, self).setUp()

        _setup()

    # def setUp

    def test_gallery_url(self):
        for key in settings.FILEBROWSER_VERSIONS:
            version_generator("1_gal.jpg", key)
        self.assertEqual(portal_service.url_of_gallery_image_version("1_gal.jpg"),
                         "http://test.com/1_gal_gallery.jpg")
        self.assertLess(
            os.path.getsize(os.path.join(settings.FILEBROWSER_MEDIA_ROOT, "1_gal_gallery.jpg")),
            os.path.getsize(os.path.join(settings.FILEBROWSER_MEDIA_ROOT, "1_gal.jpg")))

        self.assertEqual(portal_service.url_of_gallery_image_version("1_gal_ix.jpg"),
                         "http://test.com/1_gal_gallery.jpg")
        self.assertGreater(
            os.path.getsize(os.path.join(settings.FILEBROWSER_MEDIA_ROOT, "1_gal_gallery.jpg")),
            os.path.getsize(os.path.join(settings.FILEBROWSER_MEDIA_ROOT, "1_gal_ix.jpg")))

        self.assertEqual(portal_service.url_of_gallery_image_version("1_gal_smallIx.jpg"),
                         "http://test.com/1_gal_gallery.jpg")
        self.assertGreater(
            os.path.getsize(os.path.join(settings.FILEBROWSER_MEDIA_ROOT, "1_gal_gallery.jpg")),
            os.path.getsize(os.path.join(settings.FILEBROWSER_MEDIA_ROOT, "1_gal_smallIx.jpg")))

    # def test_gallery_url

# class ImagesUrlsTest