from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import re

START_RE = re.compile('<h1[^<>]+documentFirstHeading[^<>]+>') # Standard plone header
END_RE = re.compile('</h1>')

class DefaultItemView(BrowserView):
    """
    The default blog item view
    """
    
    template = ViewPageTemplateFile("default_item.pt")
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def __call__(self):
        html = self.template()
        tag = START_RE.search(html)
        if not tag:
            return html
        startpos = tag.end()
        endpos = END_RE.search(html, startpos).start()
        
        result = (html[:startpos],
                  '<a href="',
                  self.context.absolute_url(),
                  '">',
                  html[startpos:endpos],
                  '</a>',
                  html[endpos:])        
        return ''.join(result)
    