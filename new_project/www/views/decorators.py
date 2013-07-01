from functools import wraps
from bottle import redirect

from datafly.core import g

def registered_only(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if g.user:
            return f(*args, **kwargs)
        return redirect('/')
    return decorator