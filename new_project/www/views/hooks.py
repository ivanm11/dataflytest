from bottle import request

from datafly.core import g, get_assets

from models import User
from config import Config

def before_request():    
    # g - global vars for Bottle
    g._reset()    

    # global template context
    g.template_context = c = dict(        
        cache_timestamp = Config.CACHE_TIMESTAMP,
        base_url = Config.BASE_URL,
        date_format = '<strong>%B %e, %Y</strong> %I:%M %p',        
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