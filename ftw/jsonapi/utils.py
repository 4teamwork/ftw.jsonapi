import json


def pretty_json(data):
    return json.dumps(data, sort_keys=True, indent=4)


def set_json_headers(request):
    request.response.setHeader('Content-Type',
                               'application/json; charset=utf-8')
