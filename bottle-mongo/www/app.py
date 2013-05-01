from os import path
from bottle import (Bottle, Jinja2Template, TEMPLATE_PATH, static_file)

from datafly.bottle.utils import template

from config import Config, ConfigEnv

# Main App
TEMPLATE_PATH.append("./templates")
TEMPLATE_PATH.append("./")
TEMPLATE_PATH.append("./datafly")
root_app = Bottle()

from datafly.admin import admin_required

@root_app.hook('before_request')
def before_request():
    # c - template context
    c = Jinja2Template.defaults = {}
    # update if css/js changed before production deploy()
    c['cache_timestamp'] = Config.CACHE_TIMESTAMP
    c['env'] = ConfigEnv
    admin_required(c, root_app=True)

@root_app.get('/')
def index():
    return template('home.html')

from datafly.admin import app
root_app.mount('/admin/user', app)

from datafly.pages import app
root_app.mount('/admin/pages', app)

# LOCAL DEVELOPMENT

@root_app.route('/static/:filename#.*#')
def static(filename):
    d, filename = path.split(filename)
    return static_file(filename, './static/' + d + '/')

if __name__ == "__main__":
    root_app.run(host='localhost', port=8080, debug=True, reloader=True)