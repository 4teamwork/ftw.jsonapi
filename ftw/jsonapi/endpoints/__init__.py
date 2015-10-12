from ftw.jsonapi.interfaces import IAPIEndpoint
from zope.interface import implements


class Endpoint(object):
    implements(IAPIEndpoint)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def browserDefault(self, request):
        return self, ()
