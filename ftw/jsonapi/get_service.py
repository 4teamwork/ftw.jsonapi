from ftw.jsondump.interfaces import IJSONRepresentation
from plone.rest import Service
from zope.component import getMultiAdapter
import json


class GetService(Service):

    def render(self):
        json_representation = getMultiAdapter((self.context, self.request),
                                              IJSONRepresentation)
        return json.loads(json_representation.json())
