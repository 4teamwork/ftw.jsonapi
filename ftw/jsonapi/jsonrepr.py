from ftw.jsonapi.interfaces import IAPIMetadataJson
from ftw.jsonapi.utils import pretty_json
from ftw.jsondump.interfaces import IJSONRepresentation
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
import json


@implementer(IAPIMetadataJson)
@adapter(Interface)
def api_metadata_json(context, partials=('metadata',
                                         'fields',
                                         'uid')):

    json_representation = getMultiAdapter((context, context.REQUEST),
                                          IJSONRepresentation)
    data = json.loads(json_representation.json(only=partials))

    context_api_view = context.restrictedTraverse('@@api')
    data['@url'] = '/'.join((context_api_view.api_url, 'metadata'))
    return pretty_json(data)
