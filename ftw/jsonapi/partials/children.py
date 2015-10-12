from ftw.jsonapi.interfaces import IAPIRequest
from ftw.jsondump.interfaces import IPartial
from Products.CMFCore.interfaces import IFolderish
from zope.component import adapts
from zope.interface import implements


class ChildrenPartial(object):
    implements(IPartial)
    adapts(IFolderish, IAPIRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, config):
        return {'children': map(self._brain_to_item,
                                self.context.getFolderContents())}

    def _brain_to_item(self, brain):
        return {'@url': brain.getURL() + '/api/metadata',
                'id': brain.getId,
                'title': brain.Title}
