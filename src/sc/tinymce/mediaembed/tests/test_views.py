# -*- coding: utf-8 -*-

import os
import unittest2 as unittest

from zope.event import notify

from zope.component import queryMultiAdapter

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from sc.tinymce.mediaembed.testing import INTEGRATION_TESTING

from s17.media.views.events import set_media_layout

from Products.CMFPlone.tests import dummy

import sc.tinymce.mediaembed.tests

try:
    import json
except ImportError:
    import simplejson as json

dir = sc.tinymce.mediaembed.tests

MP3 = open(os.path.join(os.path.dirname(dir.__file__), 'test.mp3')).read()
MP4 = open(os.path.join(os.path.dirname(dir.__file__), 'test.mp4')).read()


class VideoListTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        self.folder.invokeFactory('File', id='f1', title='File', file=dummy.File(filename='test.mp4', data=MP4))
        self.f1 = self.folder['f1']
        event = set_media_layout(self.f1, self.portal.REQUEST)
        notify(event)

    def test_video_list_view_is_registered(self):
        view = queryMultiAdapter((self.f1, self.request), name='video_list')
        self.assertTrue(view is not None)

    def test_video_query(self):
        view = queryMultiAdapter((self.f1, self.request), name='video_list')
        video_query = view.video_query()
        if video_query:
            self.assertTrue(video_query[0].Title == 'File')
        else:
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

        self.folder.invokeFactory('File', id='v1', title='Video File', file=dummy.File(filename='test.mp4', data=MP4))
        self.v1 = self.folder['v1']
        event = set_media_layout(self.v1, self.portal.REQUEST)
        notify(event)

        self.folder.invokeFactory('File', id='a1', title='Audio File', file=dummy.File(filename='test.mp3', data=MP3))
        self.a1 = self.folder['a1']
        event = set_media_layout(self.a1, self.portal.REQUEST)
        notify(event)

    def test_media_search_view_is_registered(self):
        view = queryMultiAdapter((self.v1, self.request), name='media_search')
        self.assertTrue(view is not None)

        view = queryMultiAdapter((self.a1, self.request), name='media_search')
        self.assertTrue(view is not None)

    def test_render_video(self):
        view = queryMultiAdapter((self.v1, self.request), name='media_search')
        render = view.render(media_type='video')
        if render:
            self.assertTrue(json.loads(render)[0]['title'] == 'Video File')
        else:
            self.fail()

    def test_render_audio(self):
        view = queryMultiAdapter((self.a1, self.request), name='media_search')
        render = view.render(media_type='audio')
        if render:
            self.assertTrue(json.loads(render)[0]['title'] == 'Audio File')
        else:
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

        self.folder.invokeFactory('File', id='v1', title='Video File', file=dummy.File(filename='test.mp4', data=MP4))
        self.v1 = self.folder['v1']
        event = set_media_layout(self.v1, self.portal.REQUEST)
        notify(event)

    def test_video_list_view_is_registered(self):
        view = queryMultiAdapter((self.d1, self.request), name='tiny_media_embed')
        self.assertTrue(view is not None)

    def test_getBreadcrumbs(self):
        view = queryMultiAdapter((self.d1, self.request), name='tiny_media_embed')
        folder_breadcrumb = view.getBreadcrumbs()[1]
        self.assertTrue(folder_breadcrumb['url'] == 'http://nohost/plone/test-folder')
        self.assertTrue(folder_breadcrumb['title'] == 'test-folder')

    def test_getListing(self):
        view = queryMultiAdapter((self.d1, self.request), name='tiny_media_embed')
        result = view.getListing(filter_portal_types=['Document', ], rooted=True,
                                 document_base_url=self.folder)
        result = json.loads(result)
        self.assertTrue(result['parent_url'] == 'http://nohost/plone')
        self.assertTrue(result['path'][0]['url'] == '/plone')
        self.assertTrue(result['path'][0]['title'] == 'Plone site')
        self.assertTrue(result['path'][1]['url'] == 'http://nohost/plone/test-folder')
        self.assertTrue(result['path'][1]['title'] == 'test-folder')

    def test_render(self):
        view = queryMultiAdapter((self.v1, self.request), name='tiny_media_embed')
        result = view.render(rooted=True, document_base_url=self.folder)
        result = json.loads(result)
        items = result['items'][0]
        self.assertTrue(items['title'] == 'Video File')
        self.assertTrue(items['url'] == 'http://nohost/plone/test-folder/v1')
        self.assertTrue(items['portal_type'] == 'File')
