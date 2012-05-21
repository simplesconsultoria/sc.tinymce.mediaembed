# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import queryMultiAdapter

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from s17.tinymce.mediaembed.testing import INTEGRATION_TESTING


class VideoListTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('Document', 'd1')
        self.d1 = self.folder['d1']

    def test_video_list_view_is_registered(self):
        view = queryMultiAdapter((self.d1, self.request), name='video_list')
        self.assertTrue(view is not None)

    def test_video_query(self):
        # TODO
        self.fail()


class MediaSearchTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('Document', 'd1')
        self.d1 = self.folder['d1']

    def test_media_search_view_is_registered(self):
        view = queryMultiAdapter((self.d1, self.request), name='media_search')
        self.assertTrue(view is not None)

    def test_render(self):
        # TODO
        self.fail()


class TinyMediaEmbedTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('Document', 'd1')
        self.d1 = self.folder['d1']

    def test_video_list_view_is_registered(self):
        view = queryMultiAdapter((self.d1, self.request), name='media_search')
        self.assertTrue(view is not None)

    def test_getBreadcrumbs(self):
        # TODO
        self.fail()

    def test_getListing(self):
        # TODO
        self.fail()

    def test_render(self):
        # TODO
        self.fail()
