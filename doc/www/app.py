from os import path
from bottle import Bottle, request, redirect, abort

from datafly.core import (template, g, get_assets,
                          get_cookie, set_cookie, delete_cookie)

from config import Config, SITE_ROOT

def init_globals():    
    g._reset()    
    g.template_context = dict(        
        cache_timestamp = Config.CACHE_TIMESTAMP,
        env = Config.__name__,
        assets = get_assets()
    )    
    developer = get_cookie('developer')    
    if not developer:
        # very simple login
        password = request.query.get('password', '')        
        if password and password == Config.PASSWORD:
            set_cookie('developer', '1')
        else:
            abort(401, "Sorry, access denied.")

app = Bottle()
app.hooks.add('before_request', init_globals)

@app.get('/')
def getting_started():    
    return redirect('/getting_started')

@app.get('/logout')
def logout():
    """ for testing purposes """
    delete_cookie('developer')
    return redirect('/')

@app.get('/<slug>')
def markdown_article(slug):
    template_context = c = dict(
        title = 'Developer Docs',
        request_path = request.path
    )    
    filename = '%s.md' % slug.replace('-', '_')
    f = open(path.join(SITE_ROOT, 'markdown', filename))
    c['article'] = f.read().decode('utf-8')
    f.close()
    return template('markdown.html', **template_context)

# For local development
if __name__ == "__main__":
    from datafly.core import assets_app
    app.merge(assets_app)
    app.run(host=Config.HOST, port=Config.PORT, debug=True, reloader=True)