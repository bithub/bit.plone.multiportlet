
from zope.interface import Interface
from zope.component import adapts

from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.manager import ColumnPortletManagerRenderer

from bit.plone.multiportlet.interfaces import IContainedPortlets


class MultiPortletManagerRenderer(ColumnPortletManagerRenderer):
    adapts(Interface, IDefaultBrowserLayer,
           IBrowserView, IContainedPortlets)
    template = ViewPageTemplateFile('multi_portlet.pt')
