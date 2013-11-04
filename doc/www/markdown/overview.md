OVERVIEW
========

Please always check `www/app.py` first.  
This is the main file for your application. You will start development
server by running `python app.py` (`fab runserver` does this under virtualenv)
or, for production, uWSGI python loader will search for app variable which
is Bottle instance and callable WSGI application.

```python
  app = Bottle()

  @app.error(404)
  def page404(code):
    return template('404.html')
```

Variable `app` is the default application, doesn't have any views attached,
only error handlers (to keep this file clean and simple).  
Other applications contain views and will be merged using `Bottle.merge` method.

Whenever you mount or merge an application, Bottle creates a proxy-route on the
main-application that forwards all requests to the sub-application (important
side effect: you can't add before_request hook for default application and
expect that this hook function will be called for sub-application). That's 
why we have helper function `merge()`.

```python
  # /admin/login
  merge(app, 'datafly.views.users:users', before_request=[init_global],
      config=dict(
           redirect = '/admin/home'
      ))
```

What's happening here?

1. From `datafly.views.users` import `users` (another Bottle application with a
bunch of views attached)

2. Configure these views (optional, great for reusable views from `datafly` folder).

3. Run `init_global` function before any view from this file (usually it's something
that common for a group of views - get user from cookie, for `/admin` views:
check if user is logged in).

For example, for `/home` url:

1. Request will be forwarded to `public_app` application (url is matched to
`home()` view from this application).

2. `init_global` function is called from `views/hooks.py`

3. Finally, `home()` view is called.

Reusable apps
-------------

To share code between projects we use `/datafly` subfolder. This folder is just
a marker, convention. Don't symlink it, don't exclude from Git.

How to update `/datafly` for any *existing* project:

a) Copy modules or packages:

```bash
  "starter/new_project/www/datafly" => "www/datafly" 
  "starter/new_project/script/datafly" => "script/datafly"
```

b) Don't forget to update LESS/JS in `config/assets.py`.

c) Check if something is broken.

Group imports
-------------

Imports should be grouped in the following order:

```python
  # standard library imports and related third party imports
  from bottle import Bottle

  # DataFly packages
  from datafly.core import template

  # Local imports
  from config import Config, db
```