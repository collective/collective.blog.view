from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from collective.blog.view.interfaces import IBlogEntryRetriever

class BlogView(BrowserView):
    """
    Blog view
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def _get_brains(self):
        """Returns all the brains, without batching."""
        # XXX Could perhaps be cached on the object?
        return IBlogEntryRetriever(self.context).get_entries()
        
    def blogitems(self):
        """List blog items"""
        # XXX batching
        portal_properties = getToolByName(self.context, 'portal_properties', None)
        site_properties = getattr(portal_properties, 'site_properties', None)
        blog_view_items = site_properties.getProperty('blog_view_items', 10)
        return [x.getObject() for x in self._get_brains()[:blog_view_items]]
