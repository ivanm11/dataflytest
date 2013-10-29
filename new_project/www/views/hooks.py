from bottle import request, redirect

from datafly.core import g

from models import User, data


# before_request - all pages
def init_global():    
    c = g.template_context   

    c.update(dict(      
        layout = 'public/layout.html',        
        head = 'layout_head.html',
        scripts = 'layout_scripts.html',
        data = data       
    )) 


# before_request - admin pages
def init_admin():
    c = g.template_context
    
    g.user = c['user'] = User.get_current()
    # login required for all admin pages / API requests
    if not g.user and request.path != '/admin/login':
        return redirect('/admin/login')

    """
        By default we use the same template for simple page and admin version
        of that page.
        We change layout (header, content wrapper, footer) using layout var
    """
    c.update(dict(
        admin = True,
        admin_title = 'Starter',
        layout = 'admin/layout.html'        
    ))    