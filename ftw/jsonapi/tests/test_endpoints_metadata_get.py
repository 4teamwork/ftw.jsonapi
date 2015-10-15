from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from ftw.builder import Builder
from ftw.builder import create
from ftw.jsonapi.tests import FunctionalTestCase
from ftw.jsonapi.tests.helpers import asset
from ftw.jsondump.tests.dxitem import IDXItemSchema
from ftw.testbrowser import browsing
from ftw.testing import freeze


class TestMetadataGETEndpoint(FunctionalTestCase):

    @browsing
    def test_get_site_root(self, browser):
        browser.webdav('GET', view='api/metadata')
        self.assertDictContainsSubset(
            {'@url': '{}/api/metadata'.format(self.portal.absolute_url()),
             '_id': 'plone',
             '_path': '/plone',
             '_type': 'Plone Site'},
            browser.json)

    @browsing
    def test_POST_should_not_work(self, browser):
        browser.webdav('POST', view='api/metadata')
        self.assertEquals(404, browser.response.status_code)

    @browsing
    def test_get_AT_document(self, browser):
        self.grant('Manager')

        with freeze(datetime(2015, 8, 17, 12, 35, 22)):
            page = create(Builder('page')
                          .titled('The Page')
                          .having(text='<p>A very simple page.</p>'))

        browser.login().webdav('GET', page, view='api/metadata')
        self.assertDictContainsSubset(
            {u'@url': u'{}/the-page/api/metadata'.format(self.portal.absolute_url()),
             u'_id': u'the-page',
             u'_path': u'/plone/the-page',
             u'_type': u'Document',
             u'_class': u'Products.ATContentTypes.content.document.ATDocument',
             u'creation_date:date': u'2015/08/17 11:35:22 UTC',
             u'title': u'The Page',
             u'text': u'<p>A very simple page.</p>',
             u'text:mimetype': u'text/html'},
            browser.json)

    @browsing
    def test_get_AT_file(self, browser):
        self.grant('Manager')
        document = create(Builder('file').attach_file_containing(
            asset('helloworld.py').bytes(),
            name='helloworld.py'))

        browser.login().webdav('GET', document, view='api/metadata')
        self.assertDictContainsSubset(
            {u'@url': u'{}/file/api/metadata'.format(self.portal.absolute_url()),
             u'_path': u'/plone/file',
             u'file:download': u'{}/file/api/files/file'.format(self.portal.absolute_url()),
             u'file:filename': u'helloworld.py',
             u'file:mimetype': u'text/x-python',
             u'file:size': 20},
            browser.json)

    @browsing
    def test_get_DX_object(self, browser):
        with freeze(datetime(2015, 12, 22, 17, 19, 54)):
            item = create(
                Builder('dx item')
                .titled(u'The Dexterity Item')
                .having(description=u'This is a great item!',
                        bool_field=True,
                        choice_field='Blue',
                        date_field=date(2010, 9, 8),
                        datetime_field=datetime(2012, 12, 30, 23, 59),
                        decimal_field=2.6,
                        dottedname_field='zope.schema.interfaces.IDottedName',
                        float_field=1.3,
                        list_field=[u'foo', u'bar', u'baz'],
                        richtext_field=(IDXItemSchema['richtext_field'].fromUnicode(
                            u'<p>Hello World.</p>')),
                        text_field=u'A great text.',
                        time_field=time(23, 58, 59, 1),
                        timedelta_field=timedelta(days=2, milliseconds=1, microseconds=7),
                        uri_field='http://www.python.org/foo/bar')
                .attach_image(asset('empty.gif'))
                .attach_file(asset('helloworld.py')))

        browser.login().webdav('GET', item, view='api/metadata')

        self.assertDictContainsSubset(
            {u'@url': u'{}/the-dexterity-item/api/metadata'.format(self.portal.absolute_url()),
             u'_id': u'the-dexterity-item',
             u'_path': u'/plone/the-dexterity-item',
             u'_type': u'DXItem',

             u'bool_field': True,
             u'choice_field': u'Blue',
             u'date_field': u'2010-09-08',
             u'datetime_field': u'2012-12-30T23:59:00',
             u'decimal_field': 2.6,
             u'dottedname_field': u'zope.schema.interfaces.IDottedName',
             u'file_field:download': u'{}/the-dexterity-item/api/files/file_field'.format(self.portal.absolute_url()),
             u'file_field:filename': u'helloworld.py',
             u'file_field:mimetype': u'text/x-python',
             u'file_field:size': 20,
             u'float_field': 1.3,
             u'image_field:download': u'{}/the-dexterity-item/api/files/image_field'.format(self.portal.absolute_url()),
             u'image_field:filename': u'empty.gif',
             u'image_field:mimetype': u'image/gif',
             u'image_field:size': 42,
             u'list_field': [u'foo',
                                                                    u'bar',
                                                                    u'baz'],
             u'richtext_field': u'<p>Hello World.</p>',
             u'richtext_field:encoding': u'utf-8',
             u'richtext_field:mimeType': u'text/html',
             u'richtext_field:outputMimeType': u'text/x-html-safe',
             u'text_field': u'A great text.',
             u'time_field': u'23:58:59.000001',
             u'timedelta_field': 172800.001007,
             u'uri_field': u'http://www.python.org/foo/bar',
             u'description': u'This is a great item!',
             u'title': u'The Dexterity Item'
            },
            browser.json)

    @browsing
    def test_get_includes_children(self, browser):
        self.grant('Manager')
        folder = create(Builder('folder').titled('The Folder'))
        create(Builder('page').titled('The Page').within(folder))

        browser.login().webdav('GET', folder, view='api/metadata')
        self.assertDictContainsSubset(
            {u'children': [
                {u'title': u'The Page',
                 u'id': u'the-page',
                 u'@url': u'{}/the-folder/the-page/api/metadata'.format(self.portal.portal_url())}
            ]},
            browser.json)

    @browsing
    def test_get_includes_parent(self, browser):
        self.grant('Manager')
        folder = create(Builder('folder').titled('The Folder'))

        browser.login().webdav('GET', folder, view='api/metadata')
        self.assertDictContainsSubset(
            {u'parent':  {u'title': u'Plone site',
                          u'id': u'plone',
                          u'@url': u'{}/api/metadata'.format(self.portal.portal_url())}},
            browser.json)

    @browsing
    def test_plone_site_has_no_parent(self, browser):
        self.grant('Manager')
        browser.login().webdav('GET', view='api/metadata')
        self.assertNotIn('parent', browser.json)
