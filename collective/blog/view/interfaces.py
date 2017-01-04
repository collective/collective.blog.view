# -*- coding: utf-8 -*-
"""Module where all interfaces live."""

from zope import interface
from zope import schema


class IBlogEntryRetriever(interface.Interface):

    def get_entries():
        """Retrieves all blog entries as catalog brains."""

    typesUseViewActionInListings = schema.Tuple(
        value_type=schema.TextLine(),
        required=False,
        default=(),
        missing_value=(),
    )

    blog_types = schema.Tuple(
        value_type=schema.TextLine(),
        required=False,
        default=(),
        missing_value=(),
    )

    blog_view_items = schema.Int(
        required=False,
        default=10,
    )
