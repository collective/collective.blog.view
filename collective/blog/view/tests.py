import os
import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.Five import testbrowser
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite(products=['collective.blog.view'])

import collective.blog.view

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
    
    def test_view(self):
        # Use a browser to log into the portal:
        admin = testbrowser.Browser()
        admin.handleErrors = False
        portal_url = self.portal.absolute_url()
        admin.open(portal_url)
        admin.getControl(name='__ac_name').value = ptc.portal_owner
        admin.getControl(name='__ac_password').value = ptc.default_password
        admin.getControl('Log in').click()

        # Create a folder to act as the blog:
        admin.getLink(id='folder').click()
        admin.getControl(name='title').value = 'A Blog'
        admin.getControl(name='form.button.save').click()
        # Publish it:
        admin.getLink(id='workflow-transition-publish').click()
        # And set the blog view:
        admin.getLink(id='blog_view').click()
        # Save this url for easy access later:
        blog_url = admin.url
        
        # In the folder, create four content types, a Document, a News Item,
        # a File and an Event:
        admin.getLink(id='document').click()
        admin.getControl(name='title').value = 'A Document Blog Entry'
        admin.getControl(name='text').value = 'The main body of the Document'
        admin.getControl(name='form.button.save').click()
        admin.getLink(id='workflow-transition-publish').click()
        
        admin.open(blog_url)
        admin.getLink(id='news-item').click()
        admin.getControl(name='title').value = 'A News Item Blog Entry'
        admin.getControl(name='text').value = 'The main body of the News Item'
        thefile = admin.getControl(name='image_file')
        thefile.filename = 'testlogo1.jpg'
        thefile.value = open(testfile, 'rb')
        admin.getControl(name='form.button.save').click()
        admin.getLink(id='workflow-transition-publish').click()

        admin.open(blog_url)
        admin.getLink(id='file').click()
        admin.getControl(name='title').value = 'A File Blog Entry'
        thefile = admin.getControl(name='file_file')
        thefile.filename = 'testlogo2.jpg'
        thefile.value = open(testfile, 'rb')
        admin.getControl(name='form.button.save').click()

        admin.open(blog_url)
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
        anon.open(blog_url)
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
        self.portal.portal_properties.site_properties._setProperty(
            'blog_types', ['Document', 'News Item', 'File', 'Event'])
        anon.open(blog_url)
        self.assert_('The main body of the Event' in anon.contents)
        

def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(FunctionalTestCase),
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
