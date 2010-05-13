from zope import interface
from collective.blog.view.interfaces import IBlogEntryRetriever
from Products.CMFCore.utils import getToolByName

class FolderItemGetter:
    
    interface.implements(IBlogEntryRetriever)
    
    def __init__(self, context):
        self.context = context
        
    def get_entries(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        path = self.context.getPhysicalPath()
        return catalog.searchResults(path = path, sort_on='effective')
