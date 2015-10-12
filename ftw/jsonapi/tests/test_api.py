from ftw.jsonapi.tests import FunctionalTestCase
from ftw.testbrowser import browsing


class TestAPIView(FunctionalTestCase):

    @browsing
    def test_GET_lists_endpoints(self, browser):
        browser.webdav('GET', view='api')
        self.assertIn('endpoints', browser.json)
        metadata_get = [endpoint for endpoint in browser.json['endpoints']
                        if endpoint['method'] == 'GET' and endpoint['name'] == 'metadata']

        self.assertEquals([{
            u'@url': u'{}/api/metadata'.format(self.portal.absolute_url()),
            u'description': u'Returns the JSON representation of the metadata of the object.',
            u'method': u'GET',
            u'name': u'metadata'
        }], metadata_get)
