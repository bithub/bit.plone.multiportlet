from plone.testing import z2

from plone.app.testing import PLONE_FIXTURE, TEST_USER_ID
from plone.app.testing import PloneSandboxLayer, IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import setRoles, applyProfile

from Products.Five import security


class BitPloneMultiportletTestLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import bit.plone.multiportlet
        self.loadZCML(package=bit.plone.multiportlet)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'bit.plone.multiportlet:default')
        setRoles(portal, TEST_USER_ID, ['Manager'])
        security.newInteraction()

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'bit.plone.multiportlet')


MULTIPORTLET_TEST_FIXTURE = BitPloneMultiportletTestLayer()
MULTIPORTLET_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MULTIPORTLET_TEST_FIXTURE,),
    name="bit.plone.multiportlet:integration")
MULTIPORTLET_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MULTIPORTLET_TEST_FIXTURE,),
    name="bit.plone.multiportlet:functional")
