from ftw.builder import Builder
from ftw.builder import create
from ftw.jsonapi.tests import FunctionalTestCase
from ftw.testbrowser import browsing
import json


class TestMetadataPatchEndpoint(FunctionalTestCase):

    @browsing
    def test_patch_title_AT(self, browser):
        self.grant('Manager')
        page = create(Builder('page').titled('The Page'))

        browser.login().webdav('PATCH', page, view='api/metadata',
                               data={'data': json.dumps({'title': 'The Very First Page'})})
        self.assertEquals(200, browser.response.status_code)
        self.assertDictContainsSubset(
            {'@url': '{}/the-page/api/metadata'.format(self.portal.absolute_url()),
             'title': 'The Very First Page'},
            browser.json)

    @browsing
    def test_patch_title_DX(self, browser):
        self.grant('Manager')
        item = create(Builder('dx item').titled(u'The Item'))

        browser.login().webdav('PATCH', item, view='api/metadata',
                               data={'data': json.dumps({'title': 'The best item in town'})})
        self.assertEquals(200, browser.response.status_code)
        self.assertDictContainsSubset(
            {'@url': '{}/the-item/api/metadata'.format(self.portal.absolute_url()),
             'plone.app.dexterity.behaviors.metadata.IBasic.title': 'The best item in town'},
            browser.json)
