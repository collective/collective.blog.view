collective.blog.view
====================

This view will display the contents of the objects in a folder and the number
of comments, useful for a blog view. Default views for archetypes content is
included, and you can easily create custom views for your content, by simply
calling it ``blog_item_view``.

It supports Plone 4. Plone 3 is not officially supported, but should still work.


The development of collective.blog.view was sponsored by the 
**Bergen Public Library** - http://www.nettbiblioteket.no



Using collective.blog.view
--------------------------

All you need to use it is to add it to the dependencies of your Plone setup
in one way or another, and include the zcml.

After this the blog view can be seen by simply adding ``/blog_view`` to the end
of a folder or collection.

Although collective.blog.view doesn't need any installation, there is a
profile included. If you install this view you get `Blog View` as a view
option for all folders anc collections, easily turning any folder into a Blog
with a simple click of the button. It will also create the ``blog_view_items``
and ``blog_types`` property, see below.

Installing this profile will override any changes you have done to the view
methods of `Folder`, `Large Plone Folder` and `Collections`. It's generally
not recommended to install the profile on a heavily customized site, it's
better to make the changes manually, they are few and simple.


Settings
--------

collective.blog.view has only two settings. They are both in 
``portal_properties.site_properties``.

* **blog_view_items**: This integer property will be used as the number of
  items to show per page in the blog view. If it does not exist, it will 
  default to ten items.

* **blog_types**: This lines property will be used to contain the portal_types
  that are considered entries in the blog. If it does not exist, it will 
  default to `Document`, `News Item` and `File`.
  It's ignored when you use the blog view on a collection, all items in the
  collection will then be considered blog items.


Prettyfication
--------------

collective.blog.view is functional out of the box. But it is not *pretty*.
Attempts of making it pretty with a standard Plone site is likely to be
wasted, as most Plone sites tend to have their own content types and their
own skins. So I'm not going to add extra complexity and potential for confusion
in this case, since it's likely to not be used anyway.

To make the blog view look great on your site, you will most likely want to
create custom entry views for your content types. Simply create a view (Zope 3-
style) for your content type and call it blog_item_view. There you return the
HTML you want, without HTML and BODY tags, just the HTML snipped you need.

The default views includes the "Send This / Print This" links, and if you are
logged in also the History of th object. This is because the default view 
will use the default ATContentTypes views and their "main" macro. For 
Archetypes Content that are not standard ATContentType, the base_view will
be used. If you are using standard content types, you might want to make
custom views for these too. The procedure is the same.

Lastly, to make it prettier, adjust your css for the blog-listing, blog-item and
comment-link DIVs, so it looks good on your site.


What this product do not have
-----------------------------

There is no Plone Control Panel in this product, nor will there ever be one,
so you need to change the settings through the ZMI. There will also never be
any per-folder settings, as that would require extending the schema for 
folders or have a dedicated blog type, both which will defeat the main goal
of this product: simplicity and flexibility.

A Plone Control Panel may make sense, but will in that case end up in a
separate product, and installed separately.

This product will never use doctests to test anything besides documentation.
