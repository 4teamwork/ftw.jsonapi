from ftw.jsonapi.interfaces import IAPIEndpoint
from ftw.jsonapi.interfaces import VERBS
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.interface import implements
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound


class APIView(BrowserView):
    implements(IPublishTraverse)

    def publishTraverse(self, request, name):
        self.mark_request(request)
        endpoint = queryMultiAdapter((self.context, request),
                                     IAPIEndpoint,
                                     name=name)

        if endpoint is None:
            raise NotFound(self, name, request=request)

        return endpoint

    def mark_request(self, request):
        for verb, iface in VERBS.items():
            if request.get('REQUEST_METHOD') == verb:
                alsoProvides(request, iface)
