# -*- coding: utf-8 -*-
""" """

from Products.CMFPlone.PloneBatch import Batch
from Products.Five import BrowserView
from collective.blog.view.interfaces import IBlogEntryRetriever
try:
    from plone.app.discussion.interfaces import IConversation
    USE_PAD = True
except ImportError:
    USE_PAD = False

from plone import api


class BlogView(BrowserView):
    """
    Blog view
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

        results = api.content.find(context=self.context, portal_type='Discussion Item')
        self.portal_discussion = [x.getObject() for x in results]

    def blogitems(self):
        """List all blog items as brains"""
        # XXX Could perhaps be cached?
        year = int(self.request.form.get('year',0))
        month = int(self.request.form.get('month',0))
        return IBlogEntryRetriever(self.context).get_entries(year=year, month=month)

    def batch(self):
        b_size = api.portal.get_registry_record(
            'blog_view_items',
            interface=IBlogEntryRetriever
        )
        if not b_size:
            b_size = 10
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
        try:
            use_view = api.portal.get_registry_record(
                'typesUseViewActionInListings',
                interface=IBlogEntryRetriever
            )
        except:
            use_view = []
        url = item.getURL()
        if item.portal_type in use_view:
            return '%s/view' % url
        return url
