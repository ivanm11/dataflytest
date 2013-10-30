from bottle import Bottle, request, redirect, TemplateError

from datafly.core import g, template
from datafly.models.page import Page

admin_app = Bottle()

@admin_app.get('/admin')
def short_url():    
    url = '/admin/home' if g.user else '/admin/login'
    return redirect(url)

@admin_app.get('/admin/login')
def login():    
    if g.user:
        return redirect('/admin/home')
    return template('admin/login.html')

@admin_app.get('/admin/news')
@admin_app.get('/admin/gallery')
def custom_admin_page():    
    return template('admin/custom.html')

@admin_app.get('/admin/:page')
@admin_app.get('/admin/<section:re:(section|another-section)>/:page')
def simple_page(page, section=None):
    template_context = c = dict(
        show_editor = True
    )
    c['page_id'] = page_id = request.path.replace('/admin', '').strip('/')
    c['page'] = page = Page.get_latest(page_id)
    if page:
        c['versions'] = page.versions
    try:
        return template('%s.html' % page_id, **template_context)
    except TemplateError:
        c['default'] = True
        return template('default.html', **template_context)