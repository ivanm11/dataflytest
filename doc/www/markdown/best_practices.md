BEST PRACTICES
==============

Goal
----

- Start project from reliable template (bootstrap)

- Share Python modules and LESS/JS code between all projects
  (similiar to frameworks)

Starter.datafly.net
-----------------------------

There is a special project that we keep up to date with best practices,
experiment with new features.

```
  ssh://git@datafly.net/home/git/starter.git/new_project
```

Open this folder in your IDE / Editor while reading current page.

Reusable apps
-------------

To share code between projects we use `/datafly` subfolder. This folder is just
a marker, convention. Don't symlink it, don't exclude from Git.

How to update `/datafly` for any *existing* project:

a) Copy module or package from `starter/new_project/www/datafly`
to `www/datafly` folder.

b) Don't forget to update LESS/JS in `config.py`.

c) Check if something is broken.

Group imports
-------------

Imports should be grouped in the following order:

* Standard library imports and related third party imports
* DataFly package imports
* Local imports

```python
  from bottle import Bottle

  from datafly.core import template, assets_app

  from config import Config
  from db import init_db
```

Views
-----

Group views by creating an application anywhere in the project. Attach hooks
(before_request, login_required) to this application.

Merge with / mount to root application (`app.py:app`).

Caveats:

1) Hooks attached to root application don't work for merged/mounted
applications. That's why we attach them to all applications if needed.

2) Arrange routes very carefully, order matters:  
[http://bottlepy.org/docs/dev/routing.html#routing-order](http://bottlepy.org/docs/dev/routing.html#routing-order)  
[https://github.com/defnull/bottle/issues/452](http://bottlepy.org/docs/dev/routing.html#routing-order)

Templates
---------

Extend Jinja2 filters and globals with `www/jinja2_ext.py`:
    
```python
  extended_filters = dict(
    markdown = markdown_html
  )

  extended_globals = dict()
```

G object
--------

Global variables. Ported from *Flask* and bound to request (request.g).

[http://flask.pocoo.org/docs/api/#flask.g](http://flask.pocoo.org/docs/api/#flask.g)

Don't overuse them (for example don't modify *g.user* across multiple modules -
hard to trace).

```python
  from datafly.core import g

  def init_globals():
    g.user = User.get_current()
```

Models
------

Just subclass `Document` from `datafly.odm`:

```python
  from datafly.odm import Document

  class Page(Document):
    __collection__ = 'pages' # define MongoDB collection

  def pre_save(self): # add hooks
    self['published'] = datetime.utcnow()
```

And you still can use PyMongo if you don't need ODM features:

```python
  from db import db

  db.pages.find({'id': _id})
```

Requirements.txt
----------------

List of required packages for a project - `server/requirements.txt`.

To get a nice output for currently installed packages use:

```bash
  pip freeze -r requirements.txt > freeze.txt
```