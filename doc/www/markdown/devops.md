DEVOPS
======

Goal
----

Useful local and server deployment / orchestration commands for [Fabric](http://http://docs.fabfile.org/)
and [Ansible](http://ansible.cc)

* Setup local and remote git repositories, virtualenv

* Install and configure Nginx, uWSGI, MongoDB

* Safely deploy updates to remote production and staging env

GIT Repositories
----------------

* host - git@datafly.net

* folder - /home/git

* password - Bbw3SIJotWhE

Fabric
-------

To upload project files (and any update in the future):

```bash
  $ fab deploy:staging
  or
  $ fab ds # shortcut, no requirements.txt check
```

For production version:

```bash
  $ fab deploy:production
  or
  $ fab dp # shortcut, no requirements.txt check
```

Ansible
-------

Install Fireball for all DataFly servers:

```bash
  $ ansible-playbook starter/ansible/fireball.yaml
```

Generate Nginx vhosts, uWSGI config files.

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