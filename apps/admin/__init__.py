from bottle import Bottle, request, response, redirect, Jinja2Template

from datafly.bottle.utils import template, set_cookie, get_cookie
from config import Config, ConfigEnv

app = Bottle()

# ADMIN AREA

def before_request():
    c = Jinja2Template.defaults = {}
    c['cache_timestamp'] = Config.CACHE_TIMESTAMP
    c['env'] = ConfigEnv
    admin_required(c)

def admin_required(template_context, root_app=False):
    """ Use in before_request hook
        app.hooks.add('before_request', admin_required)
    """
    c = template_context
    auth = get_cookie("auth")
    admin_user = (auth and auth == 'admin')
    c['admin'] = admin_user
    if admin_user:
        c['installed_apps'] = Config.APPS
        return
    if root_app:
        if request.path.startswith('/admin'):
            return redirect('/admin/user/login')
    elif request.path != '/login':
        return redirect('/admin/user/login')

@app.get('/login')
def login():
    return template('admin/login.html')

@app.post('/login')
def auth():
    if (request.forms.login == Config.ADMIN_USER['login'] and
        request.forms.password == Config.ADMIN_USER['password']):
        set_cookie("auth", "admin", max_age=30*24*60*60)
        return redirect('/admin')
    else:
        return redirect('/admin/user/login')

@app.get('/logout')
def logout():
    response.delete_cookie("auth", secret=Config.SECRET, path='/')
    return redirect('/')

