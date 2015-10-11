from datetime import datetime
from ftw.builder import Builder
from ftw.builder import create
from ftw.jsonapi.tests import FunctionalTestCase
from ftw.testbrowser import browsing
from ftw.testing import freeze


class TestGetJSON(FunctionalTestCase):

    @browsing
    def test_get_site_root(self, browser):
        browser.webdav('GET', headers={'Accept': 'application/json'})
        self.assertDictContainsSubset(
            {'_id': 'plone',
             '_path': '/plone',
             '_type': 'Plone Site'},
            browser.json)

    @browsing
    def test_of_an_AT_document(self, browser):
        self.grant('Manager')

        with freeze(datetime(2015, 8, 17, 12, 35, 22)):
            page = create(Builder('page')
                          .titled('The Page')
                          .having(text='<p>A very simple page.</p>'))

        browser.login().webdav('GET', page, headers={'Accept': 'application/json'})

        self.assertDictContainsSubset(
            {'_id': 'the-page',
             '_path': '/plone/the-page',
             '_type': 'Document',
             'title': 'The Page',
             'text': '<p>A very simple page.</p>',
             'text:mimetype': 'text/html'},
            browser.json)
