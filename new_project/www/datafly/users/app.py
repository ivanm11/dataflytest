from bottle import Bottle, request, redirect

from datafly.core import g

from models import User
from views.hooks import before_request

app = Bottle()
app.hooks.add('before_request', before_request)

@app.post('/api/users/login')
def login():    
    user = User.find_one({
        'email': request.forms.email
    })
    password = request.forms.get('password', None)
    if password is None:
        # forgot password        
        if user:
            result = { 'success': 'EmailSent' }
        else:
            result = { 'error': 'EmailError' }    
    elif user and user.verify_password(password):
        # checkbox "Remember Me"
        temporary_login = 'remember' not in request.forms
        user.set_as_current(temporary=temporary_login)
        result = {
            'error': False,
            'redirect': app.config['redirect']
        }
    else:
        result = { 'error': 'LoginError' }
    return result

@app.get('/logout')
def logout(area):
    g.user.unset_current()
    return redirect('/login')
