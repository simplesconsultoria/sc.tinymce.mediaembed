# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from sc.tinymce.mediaembed.config import PROJECTNAME
from sc.tinymce.mediaembed.testing import INTEGRATION_TESTING


class TestInstall(unittest.TestCase):
    """Ensure product is properly installed
    """

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.pt = getattr(self.portal, 'portal_tinymce')

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME),
                        '%s not installed' % PROJECTNAME)

    def test_tiny_customplugins(self):
        self.assertIn('++resource++sc.tinymce.mediaembed/editor_plugin.js',
                      self.pt.customplugins)

    def test_tiny_customtoolbar(self):
        self.assertIn('mediaembed', self.pt.customtoolbarbuttons)

class TestUninstall(unittest.TestCase):
    """Ensure product is properly uninstalled
    """

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])
        self.pt = getattr(self.portal, 'portal_tinymce')

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_uninstall_tiny_customplugins(self):
        self.assertNotIn('++resource++sc.tinymce.mediaembed/editor_plugin.js',
            self.pt.customplugins)

    def test_uninstall_tiny_customtoolbar(self):
        self.assertNotIn('mediaembed', self.pt.customtoolbarbuttons)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
