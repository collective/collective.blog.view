from DateTime import DateTime
from OFS.interfaces import IFolder
from plone.app.contenttypes.content import Collection
from Products.CMFCore.utils import getToolByName
from collective.blog.view.interfaces import IBlogEntryRetriever
from zope import interface, component
from plone import api

import calendar

class FolderEntryGetter:
    """Gets blog entries in any sort of folder"""

    interface.implements(IBlogEntryRetriever)
    component.adapts(IFolder)

    def __init__(self, context):
        self.context = context

    def _base_query(self):
        portal_types = api.portal.get_registry_record(
            'blog_types',
            interface=IBlogEntryRetriever
        )
        if not portal_types:
            portal_types = ('Document', 'News Item', 'File')

        path = '/'.join(self.context.getPhysicalPath())
        return dict(path={'query': path, 'depth':1},
                    portal_type=portal_types,
                    sort_on='effective', sort_order='reverse')

    def get_entries(self, year=None, month=None):

        catalog = getToolByName(self.context, 'portal_catalog')
        query = self._base_query()
        if year:
            if month:
                lastday = calendar.monthrange(year, month)[1]
                startdate = DateTime(year, month, 1, 0, 0)
                enddate = DateTime(year, month, lastday, 23, 59, 59)
            else:
                startdate = DateTime(year, 1, 1, 0, 0)
                enddate = DateTime(year, 12, 31, 0, 0)
            query['effective'] = dict(query=(startdate, enddate),
                                      range='minmax')
        return catalog.searchResults(**query)


class TopicEntryGetter(FolderEntryGetter):
    """Gets blog entries for collections"""

    interface.implements(IBlogEntryRetriever)
    component.adapts(Collection)

    def __init__(self, context):
        self.context = context

    def get_entries(self, year=None, month=None):
        return self.context.results()
