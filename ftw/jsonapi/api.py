from ftw.jsonapi.interfaces import IAPIEndpoint
from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound


class APIView(BrowserView):
    implements(IPublishTraverse)

    def publishTraverse(self, request, name):
        endpoint = queryMultiAdapter((self.context, self.request),
                                     IAPIEndpoint,
                                     name=name)

        if endpoint is None:
            raise NotFound(self, name, request=self.request)

        return endpoint
