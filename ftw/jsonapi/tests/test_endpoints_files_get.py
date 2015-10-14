from ftw.builder import Builder
from ftw.builder import create
from ftw.jsonapi.tests import FunctionalTestCase
from ftw.jsonapi.tests.helpers import asset
from ftw.testbrowser import browsing


class TestFilesGETEndpoint(FunctionalTestCase):

    @browsing
    def test_AT_download_primaryfield_file(self, browser):
        self.grant('Manager')
        document = create(Builder('file').attach_file_containing(
            asset('helloworld.py').bytes(),
            name='helloworld.py'))

        browser.login().webdav('GET', document, view='api/files')
        self.assertEquals(200, browser.response.status_code)
        self.assertEquals('text/x-python', browser.headers.get('Content-Type'))
        self.assertEquals('print "Hello World"\n', browser.contents)

    @browsing
    def test_AT_download_explicit_field_file(self, browser):
        self.grant('Manager')
        document = create(Builder('file').attach_file_containing(
            asset('helloworld.py').bytes(),
            name='helloworld.py'))

        browser.login().webdav('GET', document, view='api/files/file')
        self.assertEquals(200, browser.response.status_code)
        self.assertEquals('text/x-python', browser.headers.get('Content-Type'))
        self.assertEquals('print "Hello World"\n', browser.contents)

    @browsing
    def test_DX_download_primaryfield_file(self, browser):
        self.grant('Manager')
        item = create(Builder('dx item')
                      .attach_file(asset('helloworld.py')))

        browser.login().webdav('GET', item, view='api/files')
        self.assertEquals(200, browser.response.status_code)
        self.assertEquals('text/x-python', browser.headers.get('Content-Type'))
        self.assertEquals('print "Hello World"\n', browser.contents)

    @browsing
    def test_DX_download_explicit_field_file(self, browser):
        self.grant('Manager')
        item = create(Builder('dx item')
                          .attach_file(asset('helloworld.py')))

        browser.login().webdav('GET', item, view='api/files/file_field')
        self.assertEquals(200, browser.response.status_code)
        self.assertEquals('text/x-python', browser.headers.get('Content-Type'))
        self.assertEquals('print "Hello World"\n', browser.contents)

    @browsing
    def test_portal_has_no_files_endpoint(self, browser):
        self.grant('Manager')
        browser.login().webdav('GET', view='api/files')
        self.assertEquals(404, browser.response.status_code)
