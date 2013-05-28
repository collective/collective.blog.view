from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.Five import BrowserView
from collective.blog.view.interfaces import IBlogEntryRetriever
try:
    from plone.app.discussion.interfaces import IConversation
    USE_PAD = True
except ImportError:
    USE_PAD = False
    
class BlogView(BrowserView):
    """
    Blog view
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal_discussion = getToolByName(self.context, 'portal_discussion')
        
    def blogitems(self):
        """List all blog items as brains"""
        # XXX Could perhaps be cached?
        year = int(self.request.form.get('year',0))
        month = int(self.request.form.get('month',0))
        return IBlogEntryRetriever(self.context).get_entries(year=year, month=month)

    def batch(self):
        portal_properties = getToolByName(self.context, 'portal_properties')
        site_properties = getattr(portal_properties, 'site_properties')
        b_size = site_properties.getProperty('blog_view_items', 10)
        b_start = self.request.form.get('b_start', 0)
        return Batch(self.blogitems(), b_size, b_start, orphan=2)

    def commentsEnabled(self, ob):
        if USE_PAD:
            conversation = IConversation(ob)
            return conversation.enabled()
        else:
            return self.portal_discussion.isDiscussionAllowedFor(ob)
        
    def commentCount(self, ob):
        if USE_PAD:
            conversation = IConversation(ob)
            return len(conversation)
        else:
            discussion = self.portal_discussion.getDiscussionFor(ob)
            return discussion.replyCount(ob)
        
    def item_url(self, item):
        portal_properties = getToolByName(self.context, 'portal_properties')
        site_properties = getattr(portal_properties, 'site_properties')
        use_view = site_properties.getProperty('typesUseViewActionInListings')
        url = item.getURL()
        if item.portal_type in use_view:
            return '%s/view' % url
        return url
