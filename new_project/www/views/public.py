from bottle import Bottle, request, abort, TemplateError

from datafly.core import template
from datafly.models.page import Page

public_app = Bottle()

@public_app.get('/')
@public_app.get('/:page')
@public_app.get('/<section:re:(news)>/:page')
def simple_page(page=None, section=None):
    if page:
        page_id = request.path.strip('/')
    else:
        page_id = 'home'
    page = Page.get_latest(page_id)    
    try:
        return template('%s.html' % page_id, page=page)        
    except TemplateError:
        if not page:
            return abort(404, "Page not found")        
        return template('default.html', page=page, page_id=page_id)