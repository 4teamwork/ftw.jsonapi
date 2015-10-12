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


class IAPIJsonRepresentation(Interface):
    """Generates a JSON representation for an object optimized for
    API responses.
    """

    def __init__(context):
        """Adapts a context.
        """

    def as_json():
        """Returns the data as json
        """


class IAPIRequest(Interface):
    """Marker for API requests.
    """


class IGET(IAPIRequest):
    """Get method
    """


class IPOST(IAPIRequest):
    """Post method
    """


class IPUT(IAPIRequest):
    """Put method
    """


class IDELETE(IAPIRequest):
    """Delete method
    """


class IOPTIONS(IAPIRequest):
    """Options method
    """


class IPATCH(IAPIRequest):
    """Patch method
    """


VERBS = {'GET': IGET,
         'POST': IPOST,
         'PUT': IPUT,
         'DELETE': IDELETE,
         'OPTIONS': IOPTIONS,
         'PATCH': IPATCH}
