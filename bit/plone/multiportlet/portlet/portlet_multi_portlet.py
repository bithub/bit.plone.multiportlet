import sys

from zope.interface import implements
from zope.component import getMultiAdapter
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.memoize.compress import xhtml_compress
from plone.portlets.utils import hashPortletInfo
from plone.app.portlets.portlets import base

from plone.portlets.interfaces\
    import IPortletAssignmentSettings, IPortletRetriever,\
    IPortletAssignmentMapping, IPortletRenderer

from bit.plone.multiportlet.interfaces import\
    IMultiPortlet, IMultiPortletRenderer


class Assignment(base.Assignment):
    implements(IMultiPortlet)
    title = u'Multi Portlet'

    def __init__(self, data):
        super(base.Assignment, self).__init__(data)
        self.portlets = data.get('portlets', {})
        self.portlet_type = data.get('portlet_type', 'simple')


class Renderer(base.Renderer):
    implements(IMultiPortletRenderer)

    @property
    def _template(self):
        if self.data.portlet_type == 'tabbed':
            return ViewPageTemplateFile('tabbed_multi_portlet.pt')
        if self.data.portlet_type == 'floated':
            return ViewPageTemplateFile('floated_multi_portlet.pt')
        return ViewPageTemplateFile('multi_portlet.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        self.updated = False

    def showPortlet(self):
        return self.data.portlets and True or False

    def portlets(self):
        mapping = getMultiAdapter(
            (self.context, self.manager),
            IPortletAssignmentMapping)
        # only include hidden portlets
        visible_portlets = {}
        [visible_portlets.__setitem__(x, y)
         for x, y in mapping.items()
         if IPortletAssignmentSettings(
                y).get('visible', True)]

        for portlet in self.data.portlets:
            if portlet not in visible_portlets:
                renderer = getMultiAdapter(
                    (self.context, self.request,
                     self.view, self.manager, mapping[portlet]),
                    IPortletRenderer)                
                hash=hashPortletInfo(
                    dict(manager=self.manager.__name__,
                         category=mapping.__category__,
                         key='/'.join(self.context.getPhysicalPath()),
                         name=mapping[portlet].__name__))
                yield dict(id=portlet,
                           renderer=renderer,
                           hash=hash)

    def safe_render(self, portlet_renderer):
        try:
            return portlet_renderer.render()
        except ConflictError:
            raise
        except Exception:
            logger.exception('Error while rendering %r' % self)
            aq_acquire(self, 'error_log').raising(sys.exc_info())
            return self.error_message()


    def get_id(self):
        return ''

    def get_class(self):
        return ''

    def get_title(self):
        return self.project.title

    def render(self):
        return xhtml_compress(self._template(self.context))


class AddForm(base.AddForm):
    form_fields = form.Fields(IMultiPortlet)
    label = u"Add multi-portlet"
    description = "A portlet containing other portlets."

    def __call__(self, data):
        return super(base.AddForm, self).__call__()

    def create(self, data):
        for portletid in data.get('portlets', []):
            portlet = self.__parent__.get(portletid, None)
            if portlet:
                settings = IPortletAssignmentSettings(portlet)
                settings['visible'] = False
        return Assignment(data)


class EditForm(base.EditForm):
    form_fields = form.Fields(IMultiPortlet)
    label = u"Edit multi-portlet"
    description = "A portlet containing other portlets."

    def __call__(self):
        return super(base.EditForm, self).__call__()

    @form.action(u"Save",
                 condition=form.haveInputWidgets,
                 name=u'save')
    def handle_save_action(self, action, data):
        for portletid in data['portlets']:
            portlet = self.__parent__.get(portletid, None)
            if portlet:
                settings = IPortletAssignmentSettings(portlet)
                settings['visible'] = False
        for portletid in self.context.portlets:
            if portletid in data['portlets']:
                continue
            portlet = self.__parent__.get(portletid, None)
            if portlet:
                settings = IPortletAssignmentSettings(portlet)
                settings['visible'] = True
        self.context.portlets = data['portlets']
        self.context.portlet_type = data['portlet_type']
