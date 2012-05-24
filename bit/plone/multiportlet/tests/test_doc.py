import unittest
import doctest

from zope.site.hooks import setHooks
from zope.site.hooks import  setSite

from plone.testing import layered
from plone.app.testing import ploneSite

from Testing.ZopeTestCase import FunctionalDocFileSuite

OPTION_FLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE

from bit.plone.multiportlet.testing import MULTIPORTLET_FUNCTIONAL_TESTING


def setUp(self):
    with ploneSite() as portal:
        setHooks()
        setSite(portal)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
            layered(
                FunctionalDocFileSuite(
                    '../README.rst',
                    optionflags=OPTION_FLAGS),
                layer=MULTIPORTLET_FUNCTIONAL_TESTING),
            ])
    return suite
