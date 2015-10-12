from ftw.jsonapi.interfaces import IAPIEndpoint
from ftw.jsonapi.interfaces import VERBS
from ftw.jsonapi.utils import pretty_json
from zope.component import getAdapters
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import noLongerProvides
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound


class APIView(BrowserView):
    implements(IPublishTraverse)

    def __call__(self):
        endpoints = [
            {'name': ep['name'],
             'method': ep['verb'],
             'description': (ep['adapter'].__doc__ or '').strip(),
             '@url': '/'.join((self.api_url, ep['name']))}
            for ep in self.get_endpoints()]

        return pretty_json({'endpoints': endpoints})

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

    @property
    def api_url(self):
        try:
            return self._api_url
        except AttributeError:
            self._api_url = self.context.absolute_url() + '/api'
        return self._api_url

    def get_endpoints(self):
        endpoints = []
        for verb, verb_iface in VERBS.items():
            for name, adapter in self.get_endpoints_for_verb(verb_iface):
                endpoints.append({'name': name,
                                  'adapter': adapter,
                                  'verb': verb})

        return endpoints

    def get_endpoints_for_verb(self, verb_iface):
        alsoProvides(self.request, verb_iface)
        try:
            return list(getAdapters((self.context, self.request), IAPIEndpoint))
        finally:
            noLongerProvides(self.request, verb_iface)
