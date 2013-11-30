PROJECT SETUP
=============

Usually we are using two versions of each project - production and staging.

Staging version is used until project is gone live and after that for
testing any new features. Staging version: `staging` Git branch, `Staging` config.

Production version: `master` Git branch, `Production` config.

Typical setup for domain names:

* [new-project.com](new-project.com)

* [staging.new-project.com](staging.new-project.com) or
  [new-project.datafly.net](new-project.datafly.net)

Get project for development
---------------------------

Please read [Requirements](/requirements) page first.

All you need to know is repository url.

```bash
  cd /home/$USER/projects
  git clone git@bitbucket.org:df-sean/1492.git
  cd 1492/script
  fab runserver   
```

If `www/config/config.py` has `SYNC = $version` attribute and your local database is empty...

```python
  class Default(object):
    SYNC = 'Staging' # for example, Staging
```

Then on first use of `fab runserver` you will automatically:

1. get a new virtualenv in `/venv` with everything installed

2. download and import database from Staging

3. download `/static/upload` from Staging

Add `www/myconfig.py` if needed (your local Development configuration, not
versioned by Git).

```bash
  # it's better to use symlinks ($developer means your short nickname)
  ln -s myconfig_$developer.py myconfig.py
  # also you can copy and edit other developer config
  www/myconfig_ep.py > www/myconfig.py
```

Configure your LiveReload compiler: put CSS files into `www/static/compiled`
folder.

New project
-----------

Please read [DataFly Starter](/datafly-starter) guide.

Copy `new_project` dir:

```bash
  $ cp -r new_project /home/$USER/projects/new
  $ cd /home/$USER/projects/new
  $ rm /home/$USER/projects/new/server/*.nginx # delete starter.datafly.net conf
```

Edit config:

```bash
  www/config/config.py # production, staging, development config
```

Add `www/myconfig.py` if needed.

```bash
  fab runserver # python app.py
```

Configure your LiveReload compiler: put CSS files into `www/static/compiled`
folder.

Deploy project to a new server
------------------------------

Edit `devops.yaml` and `hosts` in your `/script`
folder before running `fab deploy` command.

Read [DevOps](/devops) guide for more information.