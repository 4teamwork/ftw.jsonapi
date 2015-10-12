from plone import api
import json


def pretty_json(data):
    return json.dumps(data, sort_keys=True, indent=4)


def set_json_headers(request):
    request.response.setHeader('Content-Type',
                               'application/json; charset=utf-8')


def extract_json_from_request(request):
    if request.get('BODY'):
        return json.loads(request.get('BODY'))

    if request.form.get('data'):
        return json.loads(request.form.get('data'))

    items = request.form.items()
    if len(items) == 1 and items[0][1] == '':
        return json.loads(items[0][0])

    raise ValueError('Could not find data in request.')


def path_relative_to_root(path):
    portal_path = '/'.join(api.portal.get().getPhysicalPath())
    assert path.startswith(portal_path), \
        'Path is not within site root: {}'.format(path)
    return path[len(portal_path) + 1:]
