from Products.Five import fiveconfigure
from Products.Five import testbrowser
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from datetime import datetime

import collective.blog.view
import os
import unittest

try:
    from plone.app.discussion.interfaces import IConversation
    from zope.component import createObject
    USE_PAD = True
except ImportError:
    USE_PAD = False

ptc.setupPloneSite(extension_profiles=['collective.blog.view:default'])

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             collective.blog.view)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

testfile = os.path.join(os.path.dirname(__file__), 'testlogo.jpg')
        
class FunctionalTestCase(ptc.FunctionalTestCase, TestCase):
 
    def _getAdminBrowser(self):
        # Use a browser to log into the portal:
        admin = testbrowser.Browser()
        admin.handleErrors = False
        portal_url = self.portal.absolute_url()
        admin.open(portal_url)
        admin.getLink('Log in').click()
        admin.getControl(name='__ac_name').value = ptc.portal_owner
        admin.getControl(name='__ac_password').value = ptc.default_password
        admin.getControl('Log in').click()
        return admin
 
    def afterSetUp(self):
        # Create a folder to act as the blog:
        admin = self._getAdminBrowser()
        admin.getLink(id='folder').click()
        admin.getControl(name='title').value = 'A Blog'
        admin.getControl(name='form.button.save').click()
        # Publish it:
        admin.getLink(id='workflow-transition-publish').click()
        # And set the blog view:
        admin.getLink('Blog view').click()
        # Save this url for easy access later:
        self.blog_url = admin.url
        
    def test_view(self):
        # In the folder, create four content types, a Document, a News Item,
        # a File and an Event. Enable comments on the document, and enable
        # and add on the news-item. Keep the file and event comments disabled.
        # (The testing is done during Plone 3's discussion tool, because I
        # don't want to make plone.app.discussion a dependency. But maybe
        # it just should be...)
        admin = self._getAdminBrowser()
        if USE_PAD:
            admin.open(self.portal.absolute_url() + '/@@discussion-settings')
            admin.getControl(name='form.widgets.globally_enabled:list').value = True
            admin.getControl(name='form.buttons.save').click()
            
        admin.open(self.blog_url)
        admin.getLink(id='document').click()
        admin.getControl(name='title').value = 'A Document Blog Entry'
        admin.getControl(name='text').value = 'The main body of the Document'
        admin.getControl(name='allowDiscussion:boolean').value = True
        admin.getControl(name='form.button.save').click()
        admin.getLink(id='workflow-transition-publish').click()
        
        admin.open(self.blog_url)
        admin.getLink(id='news-item').click()
        admin.getControl(name='title').value = 'A News Item Blog Entry'
        admin.getControl(name='text').value = 'The main body of the News Item'
        thefile = admin.getControl(name='image_file')
        thefile.filename = 'testlogo1.jpg'
        thefile.value = open(testfile, 'rb')
        admin.getControl(name='allowDiscussion:boolean').value = True
        admin.getControl(name='form.button.save').click()
        admin.getLink(id='workflow-transition-publish').click()
        # Add a comment. Annoyingly, this can't be done with the browser,
        # because of a bug in zope.testbrowser).
        newsitem = self.portal['a-blog']['a-news-item-blog-entry']
        if USE_PAD:
            comment = createObject('plone.Comment')
            comment.title = 'Subject'
            comment.text = 'The comment text'
            conversation = IConversation(newsitem)
            conversation.addComment(comment)
        else:
            discussion = self.portal.portal_discussion.getDiscussionFor(newsitem)
            discussion.createReply('Subject', 'The comment text')
        
        # Verify that is was created:
        admin.open(admin.url)
        self.assert_('The comment text' in admin.contents)
        
        admin.open(self.blog_url)
        admin.getLink(id='file').click()
        admin.getControl(name='title').value = 'A File Blog Entry'
        thefile = admin.getControl(name='file_file')
        thefile.filename = 'testlogo2.jpg'
        thefile.value = open(testfile, 'rb')
        admin.getControl(name='form.button.save').click()

        admin.open(self.blog_url)
        admin.getLink(id='event').click()
        admin.getControl(name='title').value = 'An Event Blog Entry'
        admin.getControl(name='text').value = 'The main body of the Event'
        admin.getControl(name='form.button.save').click()
        admin.getLink(id='workflow-transition-publish').click()
        
        #############################
        ## Now, make sure things work
        #############################
        
        # First, we list the blog and check that not only the titles
        # but also the content of the blog entries is listed, also for
        # somebody that is anonymous:
        anon = testbrowser.Browser()
        anon.handleErrors = False
        anon.open(self.blog_url)
        # The document:
        self.assert_('The main body of the Document' in anon.contents)
        # The news item with image:
        self.assert_('The main body of the News Item' in anon.contents)
        self.assert_('image_mini' in anon.contents)
        # The file:
        self.assert_('at_download/file' in anon.contents)
        # But *not* the event:
        self.assert_('The main body of the Event' not in anon.contents)

        # Add Events to the content type to show in a blog:
        self.portal.portal_properties.site_properties._updateProperty(
            'blog_types', ['Document', 'News Item', 'File', 'Event'])
        anon.open(self.blog_url)
        self.assert_('The main body of the Event' in anon.contents)
        
        # There should be one and only one count of '0 Comments' in the text.
        # It belongs to the document entry.
        pos = anon.contents.find('0 Comments')
        self.assert_(pos != -1) # We found one
        pos = anon.contents.find('0 Comments', pos+1)
        self.assert_(pos == -1) # But not two
        
        # There is also a '1 Comments', which belongs to the News Item:
        self.assert_('1 Comments' in anon.contents)
        
    def test_archive(self):              
        # In the folder, create content with a varying set of publishing dates.
        admin = self._getAdminBrowser()
        dates = [datetime(2008, 2, 29, 8, 0), datetime(2008, 5, 7, 00, 0),
                 datetime(2009, 7, 9, 12, 0), datetime(2010, 1, 1, 0, 0),
                 datetime(2010, 1, 3, 12, 0), datetime(2010, 1, 7, 12, 0),
                 datetime(2010, 2, 3, 12, 0), datetime(2010, 2, 23, 12, 0),
                 datetime(2010, 3, 29, 23, 20), datetime(2010, 4, 2, 12, 0),
                 datetime(2010, 5, 21, 12, 0)]
        
        for date in dates:
            admin.open(self.blog_url)
            admin.getLink(id='document').click()
            admin.getControl(name='title').value = 'Blog Entry for %s' % date.strftime('%Y-%m-%d %H:%M')
            admin.getControl(name='text').value = 'The main body of the Document'
            admin.getControl(name='effectiveDate_year').value = [date.strftime('%Y')]
            admin.getControl(name='effectiveDate_month').value = [date.strftime('%m')]
            admin.getControl(name='effectiveDate_day').value = [date.strftime('%d')]
            admin.getControl(name='effectiveDate_hour').value = [date.strftime('%I')]
            admin.getControl(name='effectiveDate_minute').value = [date.strftime('%M')]
            admin.getControl(name='effectiveDate_ampm').value = [date.strftime('%p')]
            admin.getControl(name='form.button.save').click()
            admin.getLink(id='workflow-transition-publish').click()
            
        # Check that the portlet works:
        anon = testbrowser.Browser()
        anon.handleErrors = False
        anon.open(self.blog_url+'?year=2010&month=1')
        
        # Cut out the navigation to avoid false positives:
        contents = anon.contents[anon.contents.find('<div id="blog-listing">'):]
        contents = contents[:contents.find('class="portlet portletNavigationTree"')]
        
        self.assert_('Blog Entry for 2010-01-01 00:00' in contents)
        self.assert_('Blog Entry for 2010-01-03 12:00' in contents)
        self.assert_('Blog Entry for 2010-01-07 12:00' in contents)
        self.assert_('Blog Entry for 2010-02-03 12:00' not in contents)
        
        anon.open(self.blog_url+'?year=2009')
        contents = anon.contents[anon.contents.find('<div id="blog-listing">'):]
        contents = contents[:contents.find('class="portlet portletNavigationTree"')]
        self.assert_('Blog Entry for 2009-07-09 12:00' in contents)
        self.assert_('Blog Entry for 2010-01-01 00:00' not in contents)
        

def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(FunctionalTestCase),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
