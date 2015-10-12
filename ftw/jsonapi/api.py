from ftw.jsonapi.interfaces import IAPIEndpoint
from ftw.jsonapi.interfaces import VERBS
from ftw.jsonapi.utils import pretty_json
from ftw.jsonapi.utils import set_json_headers
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

    def __init__(self, *args, **kwargs):
        super(APIView, self).__init__(*args, **kwargs)
        # Mark the request as non-webdav request in order to allow
        # non-standard HTTP verbs such as PATCH and PUT to be processed
        # by our api.
        # We do this only when the /api view is actually traversed
        # and we can be sure that this is not a webdav request.
        self.request.maybe_webdav_client = False

    def __getattr__(self, name):
        # Since our endpoints provide IBrowserPublisher, the traversal
        # will verify the traversal by doing a hasattr with the traversed
        # endpoint name; I do not really understand why.
        # In order to make traversal happy, we make it possible to access
        # the endpoints by attribute on the api view.
        try:
            return object.__getattr__(self, name)
        except AttributeError:
            endpoint = self.get_named_endpoint(name)
            if not endpoint:
                raise
            return endpoint

    def __call__(self):
        endpoints = [
            {'name': ep['name'],
             'method': ep['verb'],
             'description': (ep['adapter'].__doc__ or '').strip(),
             '@url': '/'.join((self.api_url, ep['name']))}
            for ep in self.get_endpoints()]

        set_json_headers(self.request)
        return pretty_json({'endpoints': endpoints})

    def publishTraverse(self, request, name):
        endpoint = self.get_named_endpoint(name, request)
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

    def get_named_endpoint(self, name, request=None):
        self.mark_request(request or self.request)
        return queryMultiAdapter((self.context, request or self.request),
                                 IAPIEndpoint,
                                 name=name)

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
            return list(getAdapters((self.context, self.request),
                                    IAPIEndpoint))
        finally:
            noLongerProvides(self.request, verb_iface)
