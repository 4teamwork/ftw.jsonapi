from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing.quickinstaller import snapshots
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_ZSERVER
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig
import ftw.jsonapi.tests.builders


snapshots.disable()


class JsonAPILayer(PloneSandboxLayer):
    defaultBases = (PLONE_ZSERVER, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '  <include package="ftw.jsonapi.tests" file="profiles.zcml" />'
            '</configure>',
            context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.jsonapi.tests:dexterity')


JSONAPI_FIXTURE = JsonAPILayer()
JSONAPI_FUNCTIONAL = FunctionalTesting(
    bases=(JSONAPI_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="ftw.jsonapi:functional")
