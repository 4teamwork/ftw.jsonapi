.. contents:: Table of Contents


Links
=====

- Github: https://github.com/4teamwork/ftw.jsonapi
- Issues: https://github.com/4teamwork/ftw.jsonapi/issues
- Pypi: http://pypi.python.org/pypi/ftw.jsonapi
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.jsonapi

Examples
========

Using curl
----------
.. code-block:: python

  # get endpoints
  curl -i -uploneconf:2015 http://jsonapi.4teamwork.ch/api

  # get metadata
  curl -i -uploneconf:2015 http://jsonapi.4teamwork.ch/api/metadata
  
  # get front-page document
  curl -i -uploneconf:2015 http://jsonapi.4teamwork.ch/front-page/api/metadata

  # change title of front-page
  curl -i -uploneconf:2015 -d '{"title": "Hi there, I am an API"}' -X PATCH http://jsonapi.4teamwork.ch/front-page/api/metadata
  
  # add a news entry
  

Using python and urllib2
------------------------

.. code-block:: python

  import json
  import urllib2
  
  data = json.load(urllib2.urlopen('http://jsonapi.4teamwork.ch/api'))
  print data

  metadata = json.load(urllib2.urlopen('http://jsonapi.4teamwork.ch/api/metadata'))

  print "Listing children:"
  for c in metadata['children']:
    child_metadata = json.load(urllib2.urlopen(c['@url']))
    print 'Title: %s Type: %s' % (c['title'], child_metadata['_type'])

Using python and requests
-------------------------

.. code-block:: python

  import json
  import requests

  username = 'ploneconf'
  password = '2015'

  r = requests.get('http://jsonapi.4teamwork.ch/api', auth=(username, password))
  print r
  print r.text
  print r.json()

  r = requests.get('http://jsonapi.4teamwork.ch/api/metadata', auth=(username, password))
  print r
  metadata = r.json()

  print "Listing children:"
  for c in metadata['children']:
    child_metadata = requests.get(c['@url'], auth=(username, password)).json()
    print 'Title: %s Type: %s' % (c['title'], child_metadata['_type'])

  # let's set a new title and description on the front-page

  url = 'http://jsonapi.4teamwork.ch/front-page/api/metadata'
  payload = {'title': 'A title set by jsonapi', 'description' : 'This is a description set by jsonapi'}

  r = requests.patch(url, data=json.dumps(payload), auth=(username, password))
  print r

Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.jsonapi`` is licensed under GNU General Public License, version 2.
