# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from plone import api
from collective.blog.view.interfaces import IBlogEntryRetriever


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'collective.blog.view',
        ]

def post_install(context):
    """Post install script"""
    if context.readDataFile('collectiveblogview_default.txt') is None:
        return

    # Do something during the installation of this package
    api.portal.set_registry_record(
        'blog_types', (u'Document', u'News Item', u'File'), interface=IBlogEntryRetriever)
    api.portal.set_registry_record(
        'blog_view_items', 10, interface=IBlogEntryRetriever)
