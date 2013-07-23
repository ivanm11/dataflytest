DEVOPS
======

Goal
----

Useful local and server deployment / orchestration commands for [Fabric](http://http://docs.fabfile.org/)
and [Ansible](http://ansible.cc)

* Setup local and remote git repositories, virtualenv

* Install and configure Nginx, uWSGI, MongoDB

* Safely deploy updates to remote production and staging env

---

*Getting errors?*  
Make sure you properly configured `devops.yaml`
and `mydevops.yaml` in `script` folder.

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

Download or upload database:

```bash
  # download
  $ fab backup_db:production
  $ fab backup_db:staging
  # download, also local import operation
  $ fab get_db:production
  $ fab get_db:staging
  # upload, also remote import operation
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

Install Fireball for all DataFly servers:

```bash
  $ ansible-playbook starter/ansible/fireball.yaml
```

Generate Nginx vhosts, uWSGI config files from `devops.yaml` information.

```bash
  $ ansible-playbook script/local.yaml
```

Nginx vhosts, uWSGI config files are ready for use. If you want, you can edit
these files (special Nginx or uWSGI setup). Look into `/setup` folder.

```
  /site.nginx
  /site_staging.nginx
  /uwsgi.ini
  /uwsgi_staging.ini
```  

You are ready to install and launch Nginx, uWSGI:

```bash
  $ ansible-playbook script/server.yaml
```

To upload Nginx virtual vhosts, uWSGI configuration files from */server* local
folder to production/staging env just repeat this playbook again:

```bash
  $ ansible-playbook script/server.yaml
```