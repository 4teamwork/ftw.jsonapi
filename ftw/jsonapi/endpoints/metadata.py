from ftw.jsonapi.endpoints import Endpoint
from ftw.jsonapi.interfaces import IAPIMetadataJson
from ftw.jsonapi.interfaces import IGET
from ftw.jsonapi.utils import set_json_headers
from zope.component import adapts
from zope.interface import Interface


class GetMetadata(Endpoint):
    """Returns the JSON representation of the metadata of the object.
    """

    adapts(Interface, IGET)

    def __call__(self):
        set_json_headers(self.request)
        return IAPIMetadataJson(self.context)
