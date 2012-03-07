import logging
from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.Transform import make_config_persistent

logger = logging.getLogger('s17.tinymce.mediaembed.setuphandlers')

def isNotThisProfile(context, marker_file):
    return context.readDataFile(marker_file) is None

def setup_portal_transforms(context):
    if isNotThisProfile(context, 's17.tinymce.mediaembed.txt'): return

    logger.info('Updating portal_transform safe_html settings')

    tid = 'safe_html'

    pt = getToolByName(context, 'portal_transforms')
    if not tid in pt.objectIds(): return

    trans = pt[tid]

    tconfig = trans._config
    tconfig['style_whitelist'] = ['text-align', 'list-style-type', 'float', 
        'padding-left', 'width', 'height', 'display']

    make_config_persistent(tconfig)
    trans._p_changed = True
    trans.reload()
