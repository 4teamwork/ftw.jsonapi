from ftw.jsonapi.testing import JSONAPI_FUNCTIONAL
from ftw.testbrowser import browsing
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest2 import TestCase
import json
import transaction


def json_browsing(testcase):
    @browsing
    def enable_json(self, browser):
        browser.replace_request_header('Accept', 'application/json')
        return testcase(self, browser)
    return enable_json


class FunctionalTestCase(TestCase):
    layer = JSONAPI_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def grant(self, *roles):
        setRoles(self.portal, TEST_USER_ID, roles)
        transaction.commit()

    def assert_structure_equal(self, expected, got, msg=None):
        got = json.dumps(got, sort_keys=True, indent=4)
        expected = json.dumps(expected, sort_keys=True, indent=4)
        self.maxDiff = None
        self.assertMultiLineEqual(got, expected, msg)
