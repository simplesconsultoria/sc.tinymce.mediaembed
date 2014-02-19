from Products.CMFCore.utils import getToolByName

def uninstall(portal, reinstall=False):

    if not reinstall:

        # normal uninstall
        setup_tool = getToolByName(portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile('profile-sc.tinymce.mediaembed:uninstall')

        pt = getToolByName(portal, 'portal_tinymce')

        return "Ran all uninstall steps."
