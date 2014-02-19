from five import grok

from zope.interface import Interface

from Products.CMFCore.utils import getToolByName
from Products.TinyMCE.interfaces.utility import ITinyMCE
from zope.component import getUtility

from s17.media.views.browser import IVideo, IAudio

from Acquisition import aq_inner

from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.navigation.root import getNavigationRoot
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFCore.interfaces._content import IFolderish
from Acquisition import aq_parent

try:
    import json
except ImportError:
    import simplejson as json

grok.templatedir('templates')


class VideoList(grok.View):
    grok.context(Interface)
    grok.name('video_list')
    grok.template('video_list')
    grok.require('zope2.View')

    def video_query(self, index=''):
        """ """
        results = []
        catalog = getToolByName(self.context, 'portal_catalog')
        iface = IVideo
        videos = catalog(object_provides=iface.__identifier__,
                         sort_on='created', Title=index)

        results = videos
        return results


class MediaSearch(grok.View):
    grok.context(Interface)
    grok.name('media_search')
    grok.require('zope2.View')

    def render(self, search_for='', path='', media_type='video',
               folders=True):
        """ """
        results = []
        normalizer = getUtility(IIDNormalizer)
        object = aq_inner(self.context)

        # check if object is a folderish object, if not, get it's parent.
        if not IFolderish.providedBy(object):
            object = aq_parent(object)

        path = '/'.join(object.getPhysicalPath())

        catalog = getToolByName(self.context, 'portal_catalog')
        medias = {'video': IVideo, 'audio': IAudio}
        iface = medias[media_type]
        media_results = catalog(object_provides=iface.__identifier__,
                                sort_on='created', Title=search_for,
                                path={'query': path, 'depth': 1})

        utility = getUtility(ITinyMCE)
        folder_portal_types = []
        if folders and not search_for:
            folder_portal_types.extend(utility.containsobjects.split('\n'))
            folders_results = catalog(portal_type=folder_portal_types,
                                      sort_on='getObjPositionInParent',
                                      path={'query': path, 'depth': 1})
            media_results = folders_results + media_results

        for brain in media_results:
            results.append({
                'id': brain.getId,
                'uid': brain.UID or None,  # Maybe Missing.Value
                'url': brain.getURL(),
                'portal_type': brain.portal_type,
                'normalized_type': normalizer.normalize(brain.portal_type),
                'title': brain.Title == '' and brain.id or brain.Title,
                'icon': brain.getIcon,
                'is_folderish': brain.is_folderish,
                'itype': 'folder' if brain.is_folderish else media_type
            })

        return json.dumps(results)


class TinyMediaEmbed(grok.View):
    grok.context(Interface)
    grok.name('tiny_media_embed')
    grok.require('zope2.View')

    def getBreadcrumbs(self, path=None):
        """Get breadcrumbs"""
        result = []

        root_url = getNavigationRoot(self.context)
        root = aq_inner(self.context.restrictedTraverse(root_url))
        root_url = root.absolute_url()

        if path is not None:
            root_abs_url = root.absolute_url()
            path = path.replace(root_abs_url, '', 1)
            path = path.strip('/')
            root = aq_inner(root.restrictedTraverse(path))

        relative = aq_inner(self.context).getPhysicalPath()[len(root.getPhysicalPath()):]
        if path is None:
            # Add siteroot
            result.append({'title': root.title_or_id(), 'url': '/'.join(root.getPhysicalPath())})

        for i in range(len(relative)):
            now = relative[:i + 1]
            obj = aq_inner(root.restrictedTraverse(now))

            if IFolderish.providedBy(obj):
                if not now[-1] == 'talkback':
                    result.append({'title': obj.title_or_id(), 'url': root_url + '/' + '/'.join(now)})
        return result

    def getListing(self, filter_portal_types, rooted, document_base_url, upload_type=None, interface=''):
        """Returns the actual listing"""

        iface = interface.__identifier__ if interface else ''
        catalog_results = []
        results = {}

        object = aq_inner(self.context)
        portal_catalog = getToolByName(object, 'portal_catalog')
        normalizer = getUtility(IIDNormalizer)

        # check if object is a folderish object, if not, get it's parent.
        if not IFolderish.providedBy(object):
            object = aq_parent(object)

        if INavigationRoot.providedBy(object) or (rooted == 'True' and document_base_url[:-1] == object.absolute_url()):
            results['parent_url'] = ''
        else:
            results['parent_url'] = aq_parent(object).absolute_url()

        if rooted == 'True':
            results['path'] = self.getBreadcrumbs(results['parent_url'])
        else:
            # get all items from siteroot to context (title and url)
            results['path'] = self.getBreadcrumbs()

        # get all portal types and get information from brains
        path = '/'.join(object.getPhysicalPath())
        for brain in portal_catalog(portal_type=filter_portal_types, sort_on='getObjPositionInParent', path={'query': path, 'depth': 1}, object_provides=iface):
            catalog_results.append({
                'id': brain.getId,
                'uid': brain.UID or None,  # Maybe Missing.Value
                'url': brain.getURL(),
                'portal_type': brain.portal_type,
                'normalized_type': normalizer.normalize(brain.portal_type),
                'title': brain.Title == '' and brain.id or brain.Title,
                'icon': brain.getIcon,
                'is_folderish': brain.is_folderish,
                'i_type': str(interface)
            })

        # add catalog_ressults
        results['items'] = catalog_results

        # return results in JSON format
        return json.dumps(results)

    def render(self, rooted, document_base_url):
        """Returns the folderlisting of video objects in JSON"""

        utility = getUtility(ITinyMCE)
        image_portal_types = [u'File']
        image_portal_types.extend(utility.containsobjects.split('\n'))

        results = self.getListing(image_portal_types, rooted,
                                  document_base_url, 'File', IVideo)
        return results
