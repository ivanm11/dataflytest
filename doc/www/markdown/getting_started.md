GETTING STARTED
===============

Introduction
------------

We start with minimum amount of code and use modern tools for deployment and
client-side coding. NoSQL and No Big and Heavy Framework. This approach should
help us make custom projects fast and easily maintain them afterwards.

Tools we use
------------

*Framework*

[Bottle Microframework](http://bottle.readthedocs.org/en/release-0.11/)
(latest stable) with [Jinja 2](http://jinja.pocoo.org/docs/)

[MongoDB](http://docs.mongodb.org/manual/)
(latest stable)

[PyMongo](http://api.mongodb.org/python/current/)
(and our tiny single-file Object Document Mapper module)

[DataFly Starter](/docsdatafly-starter)
(new project boilerplate, Fabric & Ansible global scripts)

*Environment/revision control*

[Virtualenv](http://www.virtualenv.org/en/latest)
(please, no `--system-site-packages`)

[Git](http://gitref.org/index.html)

*DevOps*

[Fabric](http://docs.fabfile.org/en/1.6/)
(deployment commands)

[Ansible](http://www.ansibleworks.com/docs/gettingstarted.html)
(to manage server configuration)

*Server*

[Nginx](http://wiki.nginx.org/Main)
(latest stable)

[uWSGI](http://uwsgi-docs.readthedocs.org/en/latest/)
(latest stable, Emperor Mode)

Get project for development
---------------------------

All you need to know is repository url.

```bash
  cd /home/$USER/projects
  # password = Bbw3SIJotWhE
  git clone ssh://git@datafly.net/home/git/$PROJECT.git  
```

Example - [Doc DataFly](http://doc.datafly.net).

$PROJECT will be `doc` in this case.

After `git clone` operation view project in `/home/$USER/projects/doc`.

New project
-----------

To start use latest DataFly Starter (pull any updates) and
just copy `new_project` dir:

```bash
  $ cp -r new_project /home/$USER/projects/new
  $ cd /home/$USER/projects/new
```

Edit configuration files:

```bash
  www/config.py # production, staging, development config
  www/myconfig.py # development config overrides
```

Add `www/myconfig.py`, `www/static/upload` to `.gitignore`.

Setup & run project manually
----------------------------

Install
[latest](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/)
MongoDB.

```bash  
  cd $PROJECT
  virtualenv venv  
  source venv/bin/activate
  (venv) pip install -r server/requirements.txt
  (venv) cd www
  (venv) python app.py
```

Setup & run project with DataFly Starter
----------------------------------------

Install
[latest](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/)
MongoDB.

Please read `Project Setup` section of [DataFly Starter](/docs/datafly-starter)

```bash
  cd /$PROJECT/script
  fab venv # setup virtualenv
  fab get_db:production # import database (if you have access)
  fab app_run # python app.py
```

For new project initialize local and remote Git repository, checkout
staging branch:

```bash
  $ fab git repo 
```