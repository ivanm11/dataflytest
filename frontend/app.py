import os
import sys
from os.path import dirname, join
sys.path.append(join(dirname(__file__), 'site-packages'))

from bottle import Bottle, request, static_file
from bottle import TEMPLATE_PATH, jinja2_template as template

TEMPLATE_PATH.append('./templates')

app = Bottle()

@app.get('/js/<filename:path>')
@app.get('/less/<filename:path>')
@app.get('/static/<filename:path>')
def static(filename):
    d, filename = os.path.split(request.path)
    return static_file(filename, '.' + d + '/')

def get_vars(admin=False):
    tvars = dict(
        head = 'layout_head.html',
        scripts = 'layout_scripts.html',
        request_path = request.path,
        title = 'New Project'
    )
    tvars['layout'] = 'admin/layout.html' if admin else 'public/layout.html'
    return tvars

@app.get('/admin/news')
@app.get('/admin/gallery')
def custom_admin_page():    
    return template('admin/custom.html', **get_vars(admin=True))

@app.post('/admin/api/<template_name:path>')
def api_stub():
    return { 'error': False }

@app.get('/admin')
@app.get('/admin/<template_name:path>')
def any_admin_page(template_name='home'):    
    return template('%s.html' % template_name, **get_vars(admin=True))

@app.get('/')
@app.get('/<template_name:path>')
def any_page(template_name='home'):    
    return template('%s.html' % template_name, **get_vars())

# For local development
if __name__ == "__main__":
    app.run(host='localhost', port=8080, debug=True, reloader=True)
