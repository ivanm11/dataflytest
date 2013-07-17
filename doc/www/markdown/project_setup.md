PROJECT SETUP
=============

Get project for development
---------------------------

All you need to know is repository url.

```bash
  cd /home/$USER/projects
  # password = Bbw3SIJotWhE
  git clone ssh://git@datafly.net/home/git/$PROJECT.git  
```

Example - [Script House](http://evol.datafly.net/).

$PROJECT will be `evol` in this case.

After `git clone` operation view project in `/home/$USER/projects/evol`.

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
```

Add `www/myconfig.py` if needed (development config overrides).

Make folders (and make sure they allow write access):

```bash
    www/static/upload/img
    www/static/upload/file  
```

Also you can remove everything that you won't use for this project.

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

Please read [DataFly Starter](/datafly-starter) guide.

You need `devops.yaml`, `mydevops.yaml` files to use Fabric helpers.

```bash
  cd /$PROJECT/script
  fab venv # setup virtualenv
  fab get_db:production # import database (if you have access)
  fab runserver # python app.py
```

To initialize local and remote Git repository for new project and checkout
staging branch:

```bash
  $ fab git repo 
```