from bottle import Bottle

from datafly.core import merge, template, debug, log_errors

from config import Config, init_db
from views.hooks import init_global, init_admin

init_db()

### Main Application

app = Bottle()

@app.error(404)
def page404(code):
    return template('404.html')


### Import & configure applications

# /<page>
merge(app, 'views.public:public', hooks=[init_global])

# /admin
merge(app, 'views.admin:admin', hooks=[init_global, init_admin])

# /admin/login
merge(app, 'datafly.users.app:users', hooks=[init_global], config=dict(
    redirect = '/admin/home'
))

# /admin/api/pages, /admin/upload
merge(app, 'datafly.pages.app:editor', hooks=[init_global, init_admin])

# /admin/api/
merge(app, 'datafly.admin.app:admin_api', hooks=[init_global, init_admin])


### Development mode

if __name__ == "__main__":
    merge(app, 'datafly.core:assets')

    @app.error(500)
    def custom500(error):    
        return debug(error)

    app.run(host=Config.HOST, port=Config.PORT, debug=True, reloader=True)


### Production / Staging mode

if Config.__name__ != 'Development': 
    app = log_errors(app)
