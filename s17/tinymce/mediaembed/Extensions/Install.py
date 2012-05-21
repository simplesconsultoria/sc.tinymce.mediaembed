from Products.CMFCore.utils import getToolByName

def uninstall(portal, reinstall=False):

    if not reinstall:

        # normal uninstall
        setup_tool = getToolByName(portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-s17.tinymce.mediaembed:uninstall')

        pt = getToolByName(portal, 'portal_tinymce')

        #uninstall custom plugins
        custom_plugins = pt.customplugins.rsplit()
        custom_plugins.remove('mediaembed|/++resource++s17.tinymce.mediaembed/editor_plugin.js')
        if len(custom_plugins) == 0:
            pt.customplugins = u''
        else:
            pt.customplugins = '\n'.join(custom_plugins)

        # uninstall custom toolbar
        custom_toolbar = pt.customtoolbarbuttons.rsplit()
        custom_toolbar.remove('mediaembed')
        if len(custom_toolbar) == 0:
            pt.customtoolbarbuttons = u''
        else:
            pt.customtoolbarbuttons = '\n'.join(custom_toolbar)

        return "Ran all uninstall steps."
