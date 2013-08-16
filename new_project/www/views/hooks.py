from bottle import request, redirect

from datafly.core import g, get_assets

from models import User, data
from config import Config

def init_globals():    
    # g - global vars for Bottle
    g._reset()    

    # global template context
    g.template_context = c = dict(      
        layout = 'layout/layout.html',        
        head = 'layout/head.html',
        scripts = 'layout/scripts.html',          
        config = Config,
        base_url = Config.BASE_URL,
        data = data,
        request_path = request.path,
        request_query_string = request.query_string,    
        env = Config.__name__
    )

    if Config.__name__ == 'Development':
        c['assets'] = get_assets()

    # user from token or cookie
    token = request.query.get('t', False)
    if token:
        g.user = User.from_token(token)
        g.user.set_as_current()
    else:
        g.user = User.get_current()
    c['user'] = g.user
    

def login_required():
    if not g.user and request.path != '/admin/login':
        return redirect('/admin/login')