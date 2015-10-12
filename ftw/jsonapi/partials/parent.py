from Acquisition import aq_inner
from Acquisition import aq_parent
from ftw.jsonapi.interfaces import IAPIRequest
from ftw.jsondump.interfaces import IPartial
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope.component import adapts
from zope.interface import implements
from zope.interface import Interface


class ParentPartial(object):
    implements(IPartial)
    adapts(Interface, IAPIRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, config):
        if IPloneSiteRoot.providedBy(self.context):
            return {}

        parent = aq_parent(aq_inner(self.context))
        return {'parent': {'@url': parent.absolute_url() + '/api/metadata',
                           'id': parent.getId(),
                           'title': parent.Title()}}
