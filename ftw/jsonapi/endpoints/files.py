from ftw.jsonapi.endpoints import Endpoint
from ftw.jsonapi.interfaces import IGET
from plone.dexterity.interfaces import IDexterityContent
from zope.component import adapts
from zope.interface import alsoProvides
from zope.interface import Interface
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound


class GetFiles(Endpoint):
    """Download files.
    """

    alsoProvides(IPublishTraverse)
    adapts(Interface, IGET)

    def __init__(self, *args, **kwargs):
        super(GetFiles, self).__init__(*args, **kwargs)
        self.fieldname = None

    def __call__(self):
        if IDexterityContent.providedBy(self.context):
            return self.download_dexterity()
        else:
            return self.download_archetypes()

    def download_dexterity(self):
        view = self.context.restrictedTraverse('@@download')
        view.fieldname = self.fieldname
        return view()

    def download_archetypes(self):
        if self.fieldname:
            return self.context.getField(self.fieldname).download(self.context)
        else:
            return self.context.getPrimaryField().download(self.context)

    def publishTraverse(self, request, name):
        if self.fieldname:
            raise NotFound(self, '/'.join((self.fieldname, name)), request=request)

        self.fieldname = name
        return self
