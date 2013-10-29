DEVOPS
======

Goal
----

Useful local and server deployment / orchestration commands for
[Fabric](http://http://docs.fabfile.org/)
and [Ansible](http://ansible.cc)

* Setup local and remote virtualenv

* Install and configure Nginx, uWSGI, MongoDB

* Safely deploy updates to remote production and staging env

* Get current version from remote (database and static files)

---

Go to `/script` folder to run Fabric and Ansible commands.

Make sure you properly configured `devops.yaml` and `hosts` in your `/script`
folder.

Fabric
-------

`runserver` command is equivalent to following:

```bash  
  cd $PROJECT
  virtualenv venv  
  source venv/bin/activate
  (venv) pip install -r server/requirements.txt
  (venv) cd www
  (venv) python app.py
```

Compile assets for deployment:

```bash
  fab collect_static
```

Update packages (from `requirements.txt`) for local virtualenv:

```bash
  fab venv
```

To upload project files (and any update in the future):

```bash
  $ fab deploy:staging
  or
  $ fab ds # collect_static and deploy to staging
```

For production version:

```bash
  $ fab deploy:production
  or
  $ fab dp # collect_static and deploy to production
```

`deploy` command is smart: if remote virtualenv is absent (no `/venv` folder),
then the whole process of a "first deploy" automatically starts:

1. rsync www folder to remote

2. generate uWSGI and Nginx config files if not already exists in local /server folder

3. install Nginx, MongoDB, uWSGI if not present on server

4. new virtualenv with everything installed

5. upload database and /static/upload

It's possible to run every step above individially:

```bash  
  # 2. generate uWSGI and Nginx config files
  fab ansible:local
  # setup Accelerate mode
  fab ansible:accelerate
  # 3. Ansible: install Nginx, MongoDB, uWSGI
  fab ansible:server
  # 4. new virtualenv with everything installed
  fab remote_venv:staging
  # 5. upload database and /static/upload
  fab put_db:staging
```

Update packages (from `requirements.txt`) for remote virtualenv:

```bash
  fab remote_venv:staging
```

Set permissions on server (`www-data` user, `upload` dir),
already a part of `deploy` command:

```bash
  $ fab chmod:production
  $ fab chmod:staging  
```

Download or upload database:

```bash
  # download to local /backup folder
  $ fab backup_db:production
  $ fab backup_db:staging

  # download and import
  # (WARNING: local db will be dropped)
  $ fab get_db:production
  $ fab get_db:staging

  # upload to remote and import
  # (WARNING: remote db will be dropped)
  $ fab put_db:production
  $ fab put_db:staging
```

Ansible
-------

Generate Nginx/uWSGI configuration files from `devops.yaml` information.

```bash
  $ fab ansible:local
```

Nginx/uWSGI configuration files are ready for use.
If you want, you can edit these files (for unique Nginx or uWSGI setup).
Please look inside `/setup` folder.

```
  /site.nginx
  /site_staging.nginx
  /uwsgi.ini
  /uwsgi_staging.ini
```  

To upload Nginx/uWSGI configuration files from local */server*
folder to production/staging use:

```bash
  $ fab ansible:server
```