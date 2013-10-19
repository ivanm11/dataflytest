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

All you need to know is repository url.

```bash
  cd /home/$USER/projects
  git clone git@bitbucket.org:df-sean/script-house.git  
```

Example - [Script House](http://evol.datafly.net/).

$PROJECT will be `evol` in this case.

After `git clone` operation view project in `/home/$USER/projects/evol`.

New project
-----------

Please read [DataFly Starter](/datafly-starter) guide.

To start use latest DataFly Starter (pull any updates) and
just copy `new_project` dir:

```bash
  $ cp -r new_project /home/$USER/projects/new
  $ cd /home/$USER/projects/new
```

Edit config:

```bash
  www/config/config.py # production, staging, development config
```

Add `www/myconfig.py` if needed (development config overrides).

For existing project you can copy other developer config:

```bash
  www/myconfig_ep.py > www/myconfig.py
```

However, it's better to use symlinks ($developer means your nickname):

```bash
  ln -s myconfig_$developer.py myconfig.py
```

Create folders (and make sure they allow write access):

```bash
    www/static/upload/img
    www/static/upload/file  
```

Also you can remove everything that you won't use for this project.

Setup & run project
-------------------

Install
[latest](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/)
MongoDB.

```bash
  cd /$PROJECT/script
  fab venv # setup virtualenv
  fab get_db:production # import staging or production database (if you have access)
  fab runserver # python app.py
```

Fab `venv` and `runserver` commands are equivalent to following

```bash  
  cd $PROJECT
  virtualenv venv  
  source venv/bin/activate
  (venv) pip install -r server/requirements.txt
  (venv) cd www
  (venv) python app.py
```

Deploy project to a new server
------------------------------

You need to edit `devops.yaml` files before using Ansible and Fabric.

```bash  
  cd /$PROJECT/script
  # rsync www folder
  fab deploy:staging
  # Ansible: install Nginx, MongoDB, uWSGI
  fab ansible:local
  fab ansible:accelerate
  fab ansible:server
  # install/update packages for venv, create if needed
  fab remote_venv:staging
  fab put_db:staging # optional, if you need to upload db
```