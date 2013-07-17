from bottle import Bottle, abort

from datafly.core import template
from datafly.pages.models import Page

pages_app = Bottle()

@pages_app.get('/')
def home():    
    return template('pages/home.html')

@pages_app.get('/:page')
@pages_app.get('/<section:re:(section|another-section)>/:page')
def simple_page(page, section=None):
    _id = '%s/%s' % (section, page) if section else page
    page = Page.get_latest(_id)
    if page:
        return template('pages/simple.html', page=page)
    else:
        return abort(404, "Page not found")