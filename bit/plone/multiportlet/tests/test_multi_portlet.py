import unittest

from zope.component import getUtility, getMultiAdapter
from zope.site.hooks import setHooks, setSite

from Products.GenericSetup.utils import _getDottedName

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletAssignmentSettings

from DateTime import DateTime

from plone.testing import layered
from plone.app.portlets.tests.base import PortletsTestCase


from bit.plone.multiportlet.portlet import portlet_multi_portlet
from bit.plone.multiportlet.testing import MULTIPORTLET_FUNCTIONAL_TESTING


def _add_portlet(mapping, name, data=None):
    portlet = getUtility(IPortletType, name=name)
    addview = mapping.restrictedTraverse('+/' + portlet.addview)
    if data is not None:
        addview.createAndAdd(data=data)
    else:
        addview()

class MultiPortletTestCase(PortletsTestCase):
    _column = 'plone.leftcolumn'

    layer = MULTIPORTLET_FUNCTIONAL_TESTING

    def afterSetUp(self):
        setHooks()
        setSite(self.portal)
    
    def add_some_portlets(self, context):
        mapping = context.restrictedTraverse(
            '++contextportlets++%s' % self._column)
        for m in mapping.keys():
            del mapping[m]
        _add_portlet(
            mapping,
            'portlets.Calendar'
            )
        _add_portlet(
            mapping,
            'portlets.Events',
            {}
            )
        return mapping
        
    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, name=self._column, context=self.portal)
        assignment = assignment or portlet_multi_portlet.Assignment({})
        return getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)

class TestPortlet(MultiPortletTestCase):

    def afterSetUp(self):
        setHooks()
        setSite(self.portal)
        self.setRoles(('Manager', ))

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='portlets.MultiPortlet')
        self.assertEquals(portlet.addview, 'portlets.MultiPortlet')

    def testRegisteredInterfaces(self):
        portlet = getUtility(IPortletType, name='portlets.MultiPortlet')
        registered_interfaces = [_getDottedName(i) for i in portlet.for_]
        registered_interfaces.sort()
        self.assertEquals(['plone.app.portlets.interfaces.IColumn',
          'plone.app.portlets.interfaces.IDashboard'],
          registered_interfaces)

    def testInterfaces(self):
        portlet = portlet_multi_portlet.Assignment({})
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        _add_portlet(mapping,
                     'portlets.MultiPortlet',
                     dict(portlets=[])
                     )
        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0],
                                   portlet_multi_portlet.Assignment))

    def test_portlet_type(self):
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        _add_portlet(mapping,
                     'portlets.MultiPortlet',
                     dict(portlets=[])
                     )
        self.assertEquals(mapping['multi-portlet'].portlet_type,
                          'simple')

    def test_add_and_add_portlets(self):
        mapping = self.add_some_portlets(self.portal)
        _add_portlet(
            mapping,
            'portlets.MultiPortlet',
            dict(portlets=['calendar'])
            )        
        self.assertEquals(
            IPortletAssignmentSettings(mapping['calendar']).get('visible', True),
            False)
        self.assertEquals(
            IPortletAssignmentSettings(mapping['events']).get('visible', True),
            True)

    def testRenderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', context=self.portal)
        assignment = portlet_multi_portlet.Assignment({})
        renderer = getMultiAdapter((context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, portlet_multi_portlet.Renderer))


class TestRenderer(MultiPortletTestCase):
    _column = 'plone.rightcolumn'

    def test_empty(self):
        mapping = self.add_some_portlets(self.folder)
        _add_portlet(
            mapping,
            'portlets.MultiPortlet',
            dict(portlets=[])
            )        
        renderer = self.renderer(
            self.folder,
            assignment=mapping['multi-portlet'])
        self.assertEquals(
            renderer.render().strip(),
            '')

    def test_subportlets(self):
        mapping = self.add_some_portlets(self.folder)
        _add_portlet(
            mapping,
            'portlets.MultiPortlet',
            dict(portlets=['calendar'])
            )        
        renderer = self.renderer(
            self.folder, assignment=mapping['multi-portlet'])
        html = renderer.render()
        self.failUnless('<table class="ploneCalendar"' in html)
        self.failIf('<dl class="portlet portletEvents">' in html)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(
        layered(
            makeSuite(TestPortlet),
            layer=MULTIPORTLET_FUNCTIONAL_TESTING))
    suite.addTest(
        layered(
            makeSuite(TestRenderer),
            layer=MULTIPORTLET_FUNCTIONAL_TESTING))
    return suite
