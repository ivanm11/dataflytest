OVERVIEW
========

Please always check `www/app.py` first.  

This is the main file and starting point for your application. You can launch
development server by running `python app.py` (`fab runserver` does this under
virtualenv).

In production, uWSGI python loader will search for app variable which
is Bottle instance and callable WSGI application.

```python
  ### Main Application

  app = Bottle()

  @app.error(404)
  def page404(code):
    return template('404.html')
```

Variable `app` is the default application and doesn't have any views attached,
only error handlers (to keep this file clean and simple).  

Other applications (modules) contain views that will be added to default
application using `Bottle.merge` method (`merge` function from `datafly.core` --
wrapper).

```python
  ### Import & configure modules

  # /blog/<page>
  merge(app, 'datafly.views.blog:public',
      config = {
          'feed': {            
              'title': 'Blog',
              'desc': 'Blog about ...',
              'email': 'info@datafly.net',
              'author': 'DataFly'
          },
          'addthis_id': '0123456789',
          'fb_id': '0123456789'
  })
```

What's happening here?

1. From `datafly.views.blog` import `public_app` (another Bottle application with a
bunch of views attached)

2. Configure module (optional, great for reusable views from `datafly` folder).

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

b) Check included LESS/JS in `config/assets.py`, update if needed.

c) If something is broken `git diff` for `datafly` folder might help.

Group imports
-------------

Style guide for imports:

```python
  # standard library imports and related third party imports
  import re
  from datetime import datetime
  from bottle import Bottle
  from jinja2.filters import do_truncate

  # DataFly folder
  from datafly.core import g, template
  from datafly.models.page import Page

  # Project modules
  from config import Config, db
```