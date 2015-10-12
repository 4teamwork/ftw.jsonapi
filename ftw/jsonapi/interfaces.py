from zope.interface import Interface


class IAPIEndpoint(Interface):
    """Provider interface for an API endpoint adapter.
    """

    def __init__(context, request):
        """Adapst context and request.
        """

    def __call__():
        """Execute a request on the endpoint.
        """
