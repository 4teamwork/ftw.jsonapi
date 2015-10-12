from ftw.builder import Builder
from ftw.builder import create
from ftw.jsonapi.interfaces import IAPIRequest
from ftw.jsonapi.tests import FunctionalTestCase
from ftw.jsondump.interfaces import IPartial
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
import json


class TestParentPartial(FunctionalTestCase):

    def test_parent_partial(self):
        self.grant('Manager')
        folder = create(Builder('folder').titled('The Folder'))
        doc = create(Builder('document').titled('The Document').within(folder))

        alsoProvides(doc.REQUEST, IAPIRequest)
        partial = getMultiAdapter((doc, doc.REQUEST), IPartial,
                                  name="parent")

        config = {}
        data = partial(config)

        portal_url = self.portal.portal_url()
        self.assertEquals(
            {u'parent': {u'@url': '{}/the-folder/api/metadata'.format(portal_url),
                         u'id': u'the-folder',
                         u'title': u'The Folder'}},
            data)

        self.assert_structure_equal(json.loads(json.dumps(data)), data)
