from ftw.jsonapi.interfaces import IAPIJsonRepresentation
from ftw.jsonapi.utils import pretty_json
from ftw.jsondump.interfaces import IJSONRepresentation
from zope.component import adapts
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.interface import Interface
import json


class APIJsonRepresentation(object):
    implements(IAPIJsonRepresentation)
    adapts(Interface)

    def __init__(self, context):
        self.context = context

    def as_json(self):
        json_representation = getMultiAdapter(
            (self.context, self.context.REQUEST),
            IJSONRepresentation)
        data = json.loads(json_representation.json())

        context_api_view = self.context.restrictedTraverse('@@api')
        data['@url'] = '/'.join((context_api_view.api_url, 'metadata'))
        return pretty_json(data)
