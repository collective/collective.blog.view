from zope import interface, component
from collective.blog.view.interfaces import IBlogEntryRetriever
from Products.CMFCore.utils import getToolByName
from OFS.interfaces import IFolder
from Products.ATContentTypes.interface import IATTopic

class FolderEntryGetter:
    """Gets blog entries in any sort of folder"""
    
    interface.implements(IBlogEntryRetriever)
    component.adapts(IFolder)
    
    def __init__(self, context):
        self.context = context
        
    def get_entries(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        return catalog.searchResults(path={'query': path, 'depth':1},
                                     sort_on='effective')

    
class TopicEntryGetter:
    """Gets blog entries for collections"""
    
    interface.implements(IBlogEntryRetriever)
    component.adapts(IATTopic)
    
    def __init__(self, context):
        self.context = context
        
    def get_entries(self):
        return self.context.queryCatalog()