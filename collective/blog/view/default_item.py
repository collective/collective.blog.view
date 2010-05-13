from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class DefaultItemView(BrowserView):
    """
    The default blog item view
    """
    
    template = ViewPageTemplateFile("default_item.pt")
    headerstart = '<h1 class="documentFirstHeading">' # Standard plone header
    headerend = '</h1>'
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def __call__(self):
        html = self.template()
        startpos = html.find(self.headerstart) + len(self.headerstart)
        endpos = html.find(self.headerend, startpos)
        result = (html[:startpos],
                  '<a href="',
                  self.context.absolute_url(),
                  '">',
                  html[startpos:endpos],
                  '</a>',
                  html[endpos:])
        
        return ''.join(result)
    