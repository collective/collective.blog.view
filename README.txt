collective.blog.view
====================

This view will display the contents of the objects in a folder and the number
of comments, useful for a blog view. Default views for archetypes content is
included, and you can easily create custom views for your content, by simply
calling it "blog_item_view".


Using collective.blog.view
--------------------------

All you need to use it is to add it to the dependencies of your Plone setup
in one way or another, and include the zcml.

After this the blog view can be seen by simply adding /blog_view to the end
of a folder or collection.

Although collective.blog.view doesn't need any installation, there is a
profile included. If you install this view you get "Blog View" as a
view option for all folders anc collections, easily turning any folder into
a Blog with a simple click of the button. It will also create the 
"blog_view_items" property, see below.

Installing this profile will override any changes you have done to the
view methods of Folder, Large Plone Folder and Collections. It's generally
not recommended to install the profile on a heavily customized site, it's
better to make the changes manually, they are few and simple.


Settings
--------

collective.blog.view has only one setting. In portal_properties.site_properties
you can add an integer property called "blog_view_items". This property will
be used as the number of items to show per page in the blog view. If it does
not exist, it will default to ten items.


What this product do not have
-----------------------------

There is no Plone Control Panel in this product, nor will there ever be one,
so you need to change the settings through the ZMI. There will also never be
any per-folder settings, as that would require extending the schema for 
folders or have a dedicated blog type, both which will defeat the main goal
of this product: simplicity and flexibility.

