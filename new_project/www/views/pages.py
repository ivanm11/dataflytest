from bottle import Bottle, request, abort, TemplateError

from datafly.core import template
from datafly.pages.models import Page

pages_app = Bottle()

@pages_app.get('/')
def home():    
    return template('home.html',
                    page = Page.get_latest('home'),)

@pages_app.get('/:page')
@pages_app.get('/<section:re:(news)>/:page')
def simple_page(page=None, section=None):
    page_id = request.path.strip('/')
    page = Page.get_latest(page_id)    
    try:
        return template('%s.html' % page_id, page=page)        
    except TemplateError:
        if not page:
            return abort(404, "Page not found")        
        return template('default.html', page=page, page_id=page_id)