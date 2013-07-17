from bottle import Bottle

from datafly.core import template

from config import Config
from db import init_db
from views.hooks import init_globals, login_required

init_db()

# Main Application
app = Bottle()

@app.error(404)
def page404(code):
    return template('404.html')

### Import / Configure applications

# configure users API
from datafly.users.app import users_app
users_app.config(dict(
    redirect = '/admin/section/page'
))
users_app.hooks.add('before_request', init_globals)

# editor API
from datafly.pages.app import editor_app
editor_app.hooks.add('before_request', init_globals)
editor_app.hooks.add('before_request', login_required)

# demo - website
from views.pages import pages_app
pages_app.hooks.add('before_request', init_globals)

# demo - admin
from views.admin import admin_app
admin_app.hooks.add('before_request', init_globals)
admin_app.hooks.add('before_request', login_required)

### Merge / Mount applications

# /admin
app.merge(admin_app) 
# /admin/upload, /api/pages
app.merge(editor_app) 
# /login, /logout
app.merge(users_app) 
# /<page>
app.merge(pages_app) 

# For local development
if __name__ == "__main__":
    from datafly.core import assets_app
    app.merge(assets_app)
    app.run(host=Config.HOST, port=Config.PORT, debug=True, reloader=True)