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


class TestMetadataEndpoint(FunctionalTestCase):

    @browsing
    def test_get_site_root(self, browser):
        browser.webdav('GET', view='api/metadata')
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

        browser.login().webdav('GET', page, view='api/metadata')
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
            {u'_id': u'the-dexterity-item',
             u'_path': u'/plone/the-dexterity-item',
             u'_type': u'DXItem',

             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.bool_field': True,
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.choice_field': u'Blue',
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.date_field': u'2010-09-08',
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.datetime_field': u'2012-12-30T23:59:00',
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.decimal_field': 2.6,
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.dottedname_field': u'zope.schema.interfaces.IDottedName',
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.file_field:file': u'cHJpbnQgIkhlbGxvIFdvcmxkIgo=',
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.file_field:filename': u'helloworld.py',
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.file_field:mimetype': u'text/x-python',
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.file_field:size': 20,
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.float_field': 1.3,
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.image_field:file': u'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.image_field:filename': u'empty.gif',
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.image_field:mimetype': u'image/gif',
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.image_field:size': 42,
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.list_field': [u'foo',
                                                                    u'bar',
                                                                    u'baz'],
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.richtext_field': u'<p>Hello World.</p>',
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.richtext_field:encoding': u'utf-8',
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.richtext_field:mimeType': u'text/html',
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.richtext_field:outputMimeType': u'text/x-html-safe',
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.text_field': u'A great text.',
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.time_field': u'23:58:59.000001',
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.timedelta_field': 172800.001007,
             u'ftw.jsonapi.tests.dxitem.IDXItemSchema.uri_field': u'http://www.python.org/foo/bar',
             u'plone.app.dexterity.behaviors.metadata.IBasic.description': u'This is a great item!',
             u'plone.app.dexterity.behaviors.metadata.IBasic.title': u'The Dexterity Item'
            },
            browser.json)
