from ftw.jsonapi.endpoints import Endpoint
from ftw.jsonapi.interfaces import IGET
from ftw.jsondump.interfaces import IJSONRepresentation
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.interface import Interface


class GetMetadata(Endpoint):
    """Returns the JSON representation of the metadata of the object.
    """

    adapts(Interface, IGET)

    def __call__(self):
        json_representation = getMultiAdapter(
            (self.context, self.request),
            IJSONRepresentation)

        return json_representation.json()
