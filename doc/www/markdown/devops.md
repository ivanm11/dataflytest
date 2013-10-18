DEVOPS
======

Goal
----

Useful local and server deployment / orchestration commands for
[Fabric](http://http://docs.fabfile.org/)
and [Ansible](http://ansible.cc)

* Setup local and remote git repositories, virtualenv

* Install and configure Nginx, uWSGI, MongoDB

* Safely deploy updates to remote production and staging env

---

*Getting errors?*  
Make sure you properly configured `devops.yaml` in `script` folder.

Fabric
-------

Compile assets for deployment:

```bash
  fab collect_static
```

To upload project files (and any update in the future):

```bash
  $ fab deploy:staging
  or
  $ fab ds # shortcut, collect static, no requirements.txt check
```

For production version:

```bash
  $ fab deploy:production
  or
  $ fab dp # shortcut, collect static, no requirements.txt check
```

Permissions (`www-data` user, `upload` dir):

```bash
  $ fab chmod:production
  $ fab chmod:staging  
```

Download or upload database:

```bash
  # just download
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

Database migration:

```bash
  # always test on local db first
  (venv) python migrations/0002_fix_tz.py
  # run on production
  fab migration:production,file=0002_fix_tz.py
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

You are ready to install and launch Nginx, uWSGI:

```bash
  $ fab ansible:server
```

To upload again Nginx/uWSGI configuration files from local */server*
folder to production/staging just repeat:

```bash
  $ fab ansible:server
```