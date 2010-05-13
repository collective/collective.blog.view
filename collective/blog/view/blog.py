from Products.Five import BrowserView
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
        return [x.getObject() for x in self._get_brains()[:5]]


