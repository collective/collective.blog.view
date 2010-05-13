from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class BlogView(BrowserView):
    """
    Blog view
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    def blogitems(self):
        """List blog items"""
        # XXX batching
        catalog = getToolByName(self, 'portal_catalog')
        path = self.context.getPhysicalPath()
        results = catalog.searchResults(path = path,
                                        sort_on='effective')[:5]
        return [x.getObject() for x in results]
