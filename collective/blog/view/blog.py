from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import Batch
from collective.blog.view.interfaces import IBlogEntryRetriever

class BlogView(BrowserView):
    """
    Blog view
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        
    def blogitems(self):
        """List all blog items as brains"""
        # XXX Could perhaps be cached on the object?
        return IBlogEntryRetriever(self.context).get_entries()

    def batch(self):
        portal_properties = getToolByName(self.context, 'portal_properties', None)
        site_properties = getattr(portal_properties, 'site_properties', None)
        b_size = site_properties.getProperty('blog_view_items', 10)
        b_start = self.request.form.get('b_start', 0)
        return Batch(self.blogitems(), b_size, b_start, orphan=2)
