from ftw.builder import Builder
from ftw.builder import create
from ftw.jsonapi.interfaces import IAPIRequest
from ftw.jsonapi.tests import FunctionalTestCase
from ftw.jsondump.interfaces import IPartial
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
import json


class TestChildrenPartial(FunctionalTestCase):

    def test_children_partial(self):
        self.grant('Manager')
        folder = create(Builder('folder').titled('The Folder'))
        create(Builder('document').titled('The Document').within(folder))
        create(Builder('folder').titled('Subfolder').within(folder))

        alsoProvides(folder.REQUEST, IAPIRequest)
        partial = getMultiAdapter((folder, folder.REQUEST), IPartial,
                                  name="children")

        config = {}
        data = partial(config)

        portal_url = self.portal.portal_url()
        self.assertEquals(
            {u'children': [
                {u'@url': '{}/the-folder/the-document/api/metadata'.format(portal_url),
                 u'id': u'the-document',
                 u'title': u'The Document'},
                {u'@url': '{}/the-folder/subfolder/api/metadata'.format(portal_url),
                 u'id': u'subfolder',
                 u'title': u'Subfolder'},
            ]},
            data)

        self.assert_structure_equal(json.loads(json.dumps(data)), data)
