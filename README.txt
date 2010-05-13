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
a Blog with a simple click of the button.

