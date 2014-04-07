from bottle import Bottle, response, request, abort, TemplateError

from datafly.core import template
from datafly.models.page import Page

from config import db

public_app = Bottle()

@public_app.get('/sitemap.xml')
def sitemap():   
    urlset = []
    pages = db.pages.find({ 'current': True, 'meta.hide': { '$ne': True } })
    for page in pages:
        if page['id'] == 'home':
            continue
        urlset.append(dict(
            location = page['id'],
            lastmod = page['published'].strftime('%Y-%m-%dT%H:%M:%S'),
            changefreq = 'weekly'
        ))    
    response.headers['Content-Type'] = 'application/xml'
    return template('sitemap.html', urlset=urlset)

@public_app.get('/')
@public_app.get('/:page')
@public_app.get('/test/:page')
#def test_page(page=None):
#    page_id = re
@public_app.get('/<section:re:(news)>/:page')
def simple_page(page=None, section=None):
    page_id = request.path.strip('/') if page else 'home'
    page = Page.get_latest(page_id)   
    print('qwe') 
    try:
        return template('%s.html' % page_id, page=page)        
    except TemplateError:
        if not page:
            return abort(404, "Page not found")        
        return template('default.html', page=page, page_id=page_id)
