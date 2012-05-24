from zope.interface import Interface
from zope.component import adapts
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.browser.editmanager import\
    ContextualEditPortletManagerRenderer
from plone.app.portlets.browser.interfaces import\
    IManageContextualPortletsView

from bit.plone.multiportlet.interfaces import IContainedPortlets


class MultiPortletEditManagerRenderer(ContextualEditPortletManagerRenderer):
    """Render a portlet manager in edit mode for fraglets
    """
    adapts(Interface, IDefaultBrowserLayer,
           IManageContextualPortletsView, IContainedPortlets)
    template = ViewPageTemplateFile('multi-edit-manager-contextual.pt')

    def __init__(self, context, request, view, manager):
        ContextualEditPortletManagerRenderer.__init__(
            self, context, request, view, manager)
        self.manager = manager
        self.view = view

    def context_blacklist_status(self):
        return True

    def group_blacklist_status(self):
        return True

    def content_type_blacklist_status(self):
        return True
