from os import path
from bottle import Bottle, request, static_file

from datafly.core import template

from views.hooks import before_request
from config import Config
from db import init_db

init_db()

# Main Application
app = Bottle()
app.hooks.add('before_request', before_request)

@app.get('/')
def home():    
    return template('login.html')

# users API
from datafly.users.app import app as subapp
subapp.config(dict(
    redirect = '/'
))
app.merge(subapp)
    

# For local development

if __name__ == "__main__":
    @app.get('/js/<filename:path>')
    @app.get('/less/<filename:path>')
    @app.get('/static/<filename:path>')
    @app.get('/datafly/<filename:path>')
    def static(filename):
        d, filename = path.split(request.path)
        return static_file(filename, '.' + d + '/')

    app.run(host=Config.HOST, port=Config.PORT, debug=True, reloader=True)