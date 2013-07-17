PROJECT STRUCTURE
=================

Goal
----

- Start project from reliable template (bootstrap)

- Share Python modules and CSS/JS code between all projects
  (like using a framework)

Example - project.datafly.net
-----------------------------

There is a special project that we keep up to date with best practices,
experiment with new features and propagate changes to `new_project`.

```
  ssh://git@datafly.net/home/git/doc.git
```

Clone this repository and open `doc` folder in your IDE / Editor while
reading this guide.

Reusable apps
-------------

Copy module or package from `starter/new_project/www/datafly`
to `www/datafly` folder.

Don't forget to update LESS/JS in `config.py`.

Requirements
------------

All required packages for project are living in `server/requirements.txt`.

To get nice output for a list of currently installed packages use:

```bash
  pip freeze -r requirements.txt > freeze.txt
```