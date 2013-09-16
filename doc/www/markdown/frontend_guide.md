DEVELOPER GUIDE
===============

You will be working with Bitbucket repo and /frontend folder of a new project.

`/frontend` is a simplified Bottle / Jinja2 app, no MongoDB / Virtualenv / Pip
required. Ready to run without additional and complex setup.

Useful links
------------

Please check excellent Jinja2 docs to learn more about template language:  
[http://jinja.pocoo.org/docs/templates/](http://jinja.pocoo.org/docs/templates/)

Bootstrap 3:  
[http://getbootstrap.com/getting-started/](http://getbootstrap.com/getting-started/)

LESS:  
[http://lesscss.org/#docs](http://lesscss.org/#docs)

Setup LiveReload (compile .less file on save event and update page CSS without refresh)  
[Example - Sublime Text 3 Plugin](https://github.com/dz0ny/LiveReload-sublimetext2)

Run Application
---------------

Just after you clone repo into new folder:

1) open "frontend" folder

2) run `python app.py` command in terminal / command line.   
Please check that *Python 2.7+* (and not Python 3) installed in your OS.

For example, for OSX Lion latest 2.7 install should be easy according to this:  
[http://hackercodex.com/guide/python-virtualenv-on-mac-osx-mountain-lion-10.8/](http://hackercodex.com/guide/python-virtualenv-on-mac-osx-mountain-lion-10.8/)

```bash
  brew install python --with-brewed-openssl
```

3) open in your browser  
[http://localhost:8080/](http://localhost:8080/)

Application basics
------------------

You don't need to create new routes in `app.py`. Just create files in `/templates`
folder:

`/` => show `templates/home.html`

`/news` => show `templates/news.html`

`/news/article` => show `templates/news/article.html`

Put images into `static/img`.

For every project we have Admin area (only Python / MongoDB developer will work
on that) but you need to understand how to make pages easy to edit.

Check following links:  

* [Home page](http://localhost:8080/)

* [Home page - change text/images in Admin](http://localhost:8080/)

Edit public/admin nav:

* `templates/public/nav.html`

* `templates/admin/nav.html`

For `/frontend` app "Save and Publish" button doesn't really work - because MongoDB
backend is required. However, you can easily check how editor is working.

Define editable text in templates:

```HTML
  <div class="desc" data-clip="uniqueid">
    All content inside div with data-clip attr can be edited using Redactor WYSIWYG in Admin.
    Data-clip value should be unique.
  </div>
```

Also images can be changed on click in Admin (sometimes it's hard to create
bulletproof layout for WYSIWYG editor, separate images and text are much safer):

```HTML
  <img src="http://placehold.it/200x200" alt="Alt"
       data-clip="uniqueimgid"
       data-fit-width="200" data-fit-height="200">
```

Trick is: both Admin and Public facing pages share `div.content` (client will see & edit
this area in Admin) and use different layout.html (from `/public` and `/admin`
folders in `/templates`).

Admin and Public facing pages also share styles/js:

* `js/shared.js`

* `less/shared.less`

`<header>` and `<footer>` aren't editable in Admin so please put their CSS
into `less/public.less` file.

Consider following files and folders read-only (don't edit them):

* `templates/admin/layout.html`

* `static/admin`

Best practices
--------------

Don't nest LESS rules more than 3 times.

Use namespaces for specific page rules, e.g. `body.news`.

To test responsive/mobile layout install following extensions for Google Chrome:  

* [Dimensions](https://chrome.google.com/webstore/detail/dimensions/hdmihohhdcbejdkidbfijmfehjbnmifk)  

* [+ No scrollbars if you're not on OSX system](https://chrome.google.com/webstore/detail/no-scroll-bars-please/ahnbemfjhoibkhlijfbbjdjafbmhimdn?hl=en)

For example, test our website - [http://datafly.net](http://datafly.net)

For IE you need to download IE8, IE9, IE10.

IE8 is the most important (more bugs) and you need at least this version to test.

Download VMs, follow instructions to install:  
[http://www.modern.ie/en-us/virtualization-tools#downloads](http://www.modern.ie/en-us/virtualization-tools#downloads)

