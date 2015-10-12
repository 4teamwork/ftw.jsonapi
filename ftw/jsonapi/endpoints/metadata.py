from ftw.jsonapi.interfaces import IAPIEndpoint
from ftw.jsonapi.interfaces import IGET
from ftw.jsondump.interfaces import IJSONRepresentation
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.interface import Interface


class Metadata(object):
    implements(IAPIEndpoint)
    adapts(Interface, IGET)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        json_representation = getMultiAdapter(
            (self.context, self.request),
            IJSONRepresentation)
        return json_representation.json()
