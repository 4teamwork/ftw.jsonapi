from ftw.jsonapi.tests import FunctionalTestCase


class TestInstalled(FunctionalTestCase):

    def test_package_is_available(self):
        import ftw.jsonapi
        self.assertTrue(ftw.jsonapi)
