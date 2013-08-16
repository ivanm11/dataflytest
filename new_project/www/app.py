from bottle import Bottle

from datafly.core import template, debug

from config import Config, init_db
from views.hooks import init_globals, login_required

init_db()

# Main Application
app = Bottle()

@app.error(404)
def page404(code):
    init_globals()
    return template('404.html')

### Import / Configure applications

# /<page>
from views.pages import pages_app
# /admin
from views.admin import admin_app, init_admin
# /admin/login
from datafly.users.app import users_app
users_app.config(dict(
    redirect = '/admin/home'
))
# /admin/api/pages, /admin/upload
from datafly.pages.app import editor_app
# /admin/api/
from datafly.admin.app import admin_api_app

### Merge / Mount applications

apps = [pages_app, admin_app, users_app, editor_app, admin_api_app]
for a in apps:    
    a.hooks.add('before_request', init_globals)
    if a in (editor_app, admin_app, admin_api_app):
        a.hooks.add('before_request', init_admin)
        a.hooks.add('before_request', login_required)   
    if Config.__name__ == 'Production':
        a.catchall = False
    else:
        a.hooks.add('after_request', debug)
    app.merge(a)

# For local development
if __name__ == "__main__":
    from datafly.core import assets_app
    app.merge(assets_app)

    @app.error(500)
    def custom500(error):    
        return debug(error)

    app.run(host=Config.HOST, port=Config.PORT, debug=True, reloader=True)