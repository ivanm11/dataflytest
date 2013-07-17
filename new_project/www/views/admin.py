from bottle import Bottle, redirect

from datafly.core import template
from datafly.pages.models import Page

admin_app = Bottle()

@admin_app.get('/admin')
def home():    
    return redirect('/admin/companies')

@admin_app.get('/admin/login')
def login():    
    return template('admin/login.html')

@admin_app.get('/admin/companies')
def companies():
    return template('admin/companies.html')

@admin_app.get('/admin/:page')
@admin_app.get('/admin/<section:re:(section|another-section)>/:page')
def simple_page(page, section=None):
    template_context = c = dict(
        layout='admin/layout.html',
        editor=True
    )    
    c['id'] = _id = '%s/%s' % (section, page) if section else page
    c['page'] = Page.get_latest(_id)
    return template('pages/simple.html', **template_context)