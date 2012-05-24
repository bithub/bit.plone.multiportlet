=================
bit.plone.project
=================

Let's log in

  >>> from plone.app.testing import login, setRoles
  >>> from plone.app.testing import TEST_USER_ID, TEST_USER_NAME
  >>> setRoles(layer['portal'], TEST_USER_ID, ['Member', 'Manager'])
  >>> login(layer['portal'], TEST_USER_NAME)

The multi portlet
-----------------

  >>> from zope.component import getUtility 
  >>> from plone.portlets.interfaces import IPortletType
  >>> portlet = getUtility(IPortletType, 'portlets.MultiPortlet')
  >>> portlet.addview
  'portlets.MultiPortlet'



Portlet types
-------------

There are several templates for rendering the multiportlet.

These are currently hardcoded in a vocabulary (should be adapted)
