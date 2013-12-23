TEMPLATES AND STATIC ASSETS
===========================

Instead of manually defining links to CSS files in the `<head>` and
JS in the `<script>` before body, please edit `www/config/assets.py`

```python
  CSS = {
    'public': [
        'less/bootstrap-public',    
        ...
        'less/public',        
        'less/shared'
    ],
  ...
  JS = {
    ...
    'admin': [
        'datafly/coffee/editor',
        ...
        'js/shared',
        'js/admin'
    ]
  ...
```

You should edit LESS files in `www/less` folder and JS in `www/js`. All
these files would be concatted, compiled and minified to `/static/compiled`
folder (while running `fab collect_static` or `fab ds`, `fab dp` commands).

Make sure your IDE / Editor compile any LESS / CoffeeScript file to
`static/compiled` (usually files are compiled to the same folder)
and exclude that folder from IDE / Editor. `static/compiled` is still included
in Git - to avoid compile all step on first run after `git clone [some
project]`.

For development mode you have all these files served by development server
but for production and staging only `/static` folder is served by Nginx as
static content.

You can change paths for base HTML template and partials in `views/hooks.py` but
usually url and templates are mapped this way:

```bash
  '\page' => simple_page() in views/public.py
  templates/home.html + templates/public/layout.html

  '\admin\page' => simple_page() in views/admin.py
  templates/home.html + datafly/templates/admin/layout.html

  layout_head.html and layout_scripts.html are shared between public and admin area
```

You should edit `templates/public/layout.html` according to given design spec
and PSD.

For admin we have default layout - `datafly/templates/admin/layout.html`

Define editable text in templates (`<div>` and data-clip attribute are required):

```django
  <div class="desc" data-clip="uniqueid">
    {% if page %}
      {{ page['uniqueid'] }}
    {% else %}
      All content inside div with data-clip attr can be edited using Redactor WYSIWYG in Admin.
      Data-clip value should be unique.
    {% endif %} 
  </div>
```

Also images can be changed on click in Admin (sometimes it's hard to create
bulletproof layout for WYSIWYG editor, separate images and text are much safer):

```django
  <img src="{{ page|getkey('img.uniqueimgid') or 'http://placehold.it/200x200' }}"
       alt="Alt"
       data-clip="uniqueimgid"
       data-fit-width="200" data-fit-height="200">
```

However it's nicer to use predefined Jinja2 macros:

```django
  {# before extends layout #}
  {% import 'editor.html' as editor with context %}

  {{ editor.img('uniqueimgid', 'http://placehold.it/200x200',
                width="200", height="200") }}

  {% call editor.html('uniqueid', class='desc') %}
    Text can be changed
  {% endcall %}  

```

Filters and globals
-------------------

Extend Jinja2 filters and globals with `utils/jinja2_ext.py`:
    
```python
  extended_filters = dict(
    markdown = markdown_html
  )

  extended_globals = dict()
```