VIEWS
=====

We have a concept of public facing pages (any user can view those pages) and a
corresponding admin area (only admin user can access and edit content from public
facing pages there). A lot of files and folders named that way:

```bash
  views/public.py
  views/admin.py
  less/public.less
  less/admin.less
  js/public.js
  js/admin.js
  templates/public/nav.html
  templates/admin/nav.html
```

Trick is: both Admin and Public facing pages share `div.content` (admin user will
see & edit this area in Admin) and use different layout.html (from `/public` and
`/admin` folders in `/templates`, `/datafly/templates`).

LESS and JS files for shared content between `public` and `admin` (usually for
content inside `div.content`):

```bash
    css/shared.less
    js/shared.js
```

For simple pages (admin can edit text in some areas and update images) you
don't need to create new views. `views/public.py` and `views/admin.py` 
already did everything for you:

```bash
  `/` => show `templates/home.html`
  `/admin/home` => show `templates/home.html` (admin layout)
  `/about` => show `templates/about.html`
  `/admin/about` => show `templates/about.html` (admin layout)  
```

G object
--------

Global variables. Ported from *Flask* and bound to request (request.g).

[http://flask.pocoo.org/docs/api/#flask.g](http://flask.pocoo.org/docs/api/#flask.g)

Use them carefully (don't modify *g.user* implicitly, for example in `/models` -
hard to trace).

```python
  from datafly.core import g

  # before_request - admin pages
  def init_admin():
    c = g.template_context
    g.admin = c['user'] = Admin.get_current()
    # login required for all admin pages / API requests
    if not g.admin and request.path != '/admin/login':
        return redirect('/admin/login')
```

Caveats
-------

Arrange routes very carefully, order matters:  
[http://bottlepy.org/docs/dev/routing.html#routing-order](http://bottlepy.org/docs/dev/routing.html#routing-order)  
[https://github.com/defnull/bottle/issues/452](http://bottlepy.org/docs/dev/routing.html#routing-order)
