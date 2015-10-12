from collective.transmogrifier.transmogrifier import Transmogrifier
from ftw.jsonapi.endpoints import Endpoint
from ftw.jsonapi.interfaces import IAPIMetadataJson
from ftw.jsonapi.interfaces import IGET
from ftw.jsonapi.interfaces import IPATCH
from ftw.jsonapi.utils import extract_json_from_request
from ftw.jsonapi.utils import path_relative_to_root
from ftw.jsonapi.utils import set_json_headers
from plone import api
from Products.CMFCore.interfaces import IContentish
from zope.component import adapts
from zope.interface import Interface


class GetMetadata(Endpoint):
    """Returns the JSON representation of the metadata of the object.
    """

    adapts(Interface, IGET)

    def __call__(self):
        set_json_headers(self.request)
        return IAPIMetadataJson(self.context)


class PatchMetadata(Endpoint):
    """Update field values of an object.
    """

    adapts(IContentish, IPATCH)

    def __call__(self):
        item = extract_json_from_request(self.request)
        self.validate(item)
        item['_path'] = path_relative_to_root(
            '/'.join(self.context.getPhysicalPath()))
        self.transmogrify(item)
        set_json_headers(self.request)
        return IAPIMetadataJson(self.context)

    def validate(self, item):
        assert isinstance(item, dict), 'Item is not a dict'
        assert '_id' not in item, '"_id" is not allowed'
        assert '_path' not in item, '"_path" is not allowed'

    def transmogrify(self, item):
        mogrifier = Transmogrifier(api.portal.get())
        mogrifier(u'ftw.inflator.creation.single_item_content_creation',
                  jsonsource=dict(item=item))
