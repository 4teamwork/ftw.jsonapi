from Products.Archetypes.BaseContent import BaseContent
from zope.component.interfaces import ComponentLookupError
from zope.event import notify
from zope.traversing.interfaces import BeforeTraverseEvent


def ArchetypesContent__before_publishing_traverse__(self, arg1, arg2=None):
        """Pre-traversal hook that stops traversal to prevent the default view
           to be appended. Appending the default view will break REST calls.
        """
        REQUEST = arg2 or arg1

        from plone.rest.interfaces import IAPIRequest
        if IAPIRequest.providedBy(REQUEST):
            # Copied of CMFCore PortalObject
            try:
                notify(BeforeTraverseEvent(self, REQUEST))
            except ComponentLookupError:
                # allow ZMI access, even if the portal's site manager is
                # missing
                pass
            return

        super(BaseContent, self).__before_publishing_traverse__(
            arg1, arg2)
