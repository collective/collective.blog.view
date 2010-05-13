from zope import interface

class IBlogEntryRetriever(interface.Interface):
        
    def get_entries():
        """Retrieves all blog entries as catalog brains."""
