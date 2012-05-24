import base64

from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.portlets.interfaces import IPortletAssignmentSettings

class PortletsVocabulary(object):
    """Vocabulary factory for Portlets.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        
        portlets = []
        if hasattr(context, 'portlets'):
            portlets = context.portlets
            for portlet in portlets:
                if not portlet in context.__parent__:
                    context.portlets.remove(portlet)


        possible = {}
        for k, v in context.__parent__.items():
            if v == context:
                continue
            settings = IPortletAssignmentSettings(v)
            if k in portlets:
                possible[k] = v                
            if settings.get('visible', True):
                possible[k] = v
                if k in portlets:
                    context.portlets.remove(k)
        
        return SimpleVocabulary(
            [SimpleTerm(value=k, token=base64.b64encode(k), title=v.title)
             for k, v in possible.items()])

PortletsVocabularyFactory = PortletsVocabulary()


class MultiPortletTypeVocabulary(object):
    """Vocabulary factory for MultiPortletType.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        multi_types = dict(simple='Simple',
                           tabbed='Tabbed',
                           accordion='Accordion',
                           floated='Floated',
                           )        
        return SimpleVocabulary(
            [SimpleTerm(value=k, token=base64.b64encode(k), title=v)
             for k, v in multi_types.items()])

MultiPortletTypeVocabularyFactory = MultiPortletTypeVocabulary()
