from zope.interface import Interface as I
from zope import schema

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.interfaces import IColumn


class IContainedPortlets(IColumn):
    """manager for rendering portlets
    """


class IMultiPortlet(IPortletDataProvider):
    """ Portlet for grouping other portlets """

    portlet_type = schema.Choice(
        title=u"Portlet type",
        required=False,
        default='simple',
        source='bit.plone.multiportlet.vocabulary.MultiPortletType')

    portlets = schema.List(
        title=u"Portlets",
        required=False,
        value_type=schema.Choice(
            source='bit.plone.multiportlet.vocabulary.Portlets',
            required=False))


class IMultiPortletRenderer(I):
    pass
