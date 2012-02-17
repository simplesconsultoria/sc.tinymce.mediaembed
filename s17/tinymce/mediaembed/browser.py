from five import grok

from zope.interface import Interface

from Products.CMFCore.utils import getToolByName

from s17.media.views.browser import IVideo, IAudio

grok.templatedir("templates")


class VideoList(grok.View):
    grok.context(Interface)
    grok.name("video_list")
    grok.template('video_list')
    grok.require("zope2.View")

    def video_query(self, index=''):
        """ """
        results = []
        catalog = getToolByName(self.context, 'portal_catalog')
        iface = IVideo
        videos = catalog(object_provides=iface.__identifier__, 
                            sort_on='created', Title=index)

        results = videos
        return results
