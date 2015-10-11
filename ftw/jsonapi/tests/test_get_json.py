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
    def test_get_AT_document(self, browser):
        self.grant('Manager')

        with freeze(datetime(2015, 8, 17, 12, 35, 22)):
            page = create(Builder('page')
                          .titled('The Page')
                          .having(text='<p>A very simple page.</p>'))

        browser.login().webdav('GET', page, headers={'Accept': 'application/json'})
        self.assertDictContainsSubset(
            {u'_id': u'the-page',
             u'_path': u'/plone/the-page',
             u'_type': u'Document',
             u'_class': u'Products.ATContentTypes.content.document.ATDocument',
             u'creation_date:date': u'2015/08/17 14:35:22 GMT+3',
             u'title': u'The Page',
             u'text': u'<p>A very simple page.</p>',
             u'text:mimetype': u'text/html'},
            browser.json)
