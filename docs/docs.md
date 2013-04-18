<title>Datafly Starter Documentation</title>
<link href="css/docs.css" rel="stylesheet">
<script src="js/jquery-2.0.0b1.js"></script>
<script src="js/docs.js"></script>

DATAFLY STARTER
===============

1. [Goals](#chapter1)
2. [Requirements](#chapter2)
3. [New Project](#chapter3)
4. [Server](#chapter4)

Goals
-----

1. Useful local & server commands for [Fabric](http://http://docs.fabfile.org/)
   and [Ansible](http://ansible.cc)

    1.1 Setup local and remote git repositories, add staging branch

    1.2 Install and configure nginx/uwsgi or apache/mod_wsgi

2. Start project from template (ex. *bottle_mongo*)

3. Shared python modules and css/js files between all Datafly projects.

Requirements
------------

Please, install latest versions of Fabric, Ansible and all required dependencies
globally:

    $ sudo pip install fabric --upgrade
    $ sudo pip install paramiko PyYAML jinja2 ansible --upgrade

This is required for Ansible Fireball mode (fast connection over 0mq):

    $ sudo pip install pyzmq pyasn1 PyCrypto python-keyczar --upgrade

If you're planning to edit and compile docs, install
[markdown2](https://github.com/trentm/python-markdown2) package globally:

    $ sudo pip install markdown2 --upgrade

    # compile docs with fabric
    $ fab docs

Add all servers to /etc/ansible/hosts file:

    [local]
    localhost

    [datafly]
    96.126.102.11
    192.155.82.246

    [rme]
    96.126.102.11

    [mas]
    192.155.82.246

New project
-----------

Make new project dir:

    $ mkdir newproject && cd newproject

You can clone Datafly Starter repository inside it:

    $ git clone ssh://root@96.126.102.11/home/datafly/git/datafly.git

Or simply make a symbolic link to existing local Datafly Starter path:

    $ ln -s ~/projects/datafly datafly

Copy project files and setup virtualenv:

    $ cd datafly/fabric
    $ fab new:bottle-mongo

Or if you are using Datafly Starter via symlink:

    $ fab new:bottle-mongo --set root_dir="$(pwd)"

Then you should edit variables in */script* files:

    /script/fabfile.py
    /script/local.yaml
    /script/fireball.yaml
    /script/server.yaml

To copy Nginx vhosts, uWSGI config files from templates to */server* folder:

    $ ansible-playbook script/local.yaml

Nginx vhosts, uWSGI config files are ready for use. If you want, you can edit
this files (for special Nginx or uWSGI setup).

To run project locally use virtualenv:

    $ cd www
    $ ../venv/bin/python app.py

Initialize Git repository:

    $ cd script
    $ fab git repo

To upload project files (and any update in the future):

    $ cd script
    $ fab deploy:staging

For production version:

    $ fab deploy:production

*To-Do*:

> maybe rewrite 'fab deploy' to Ansible playbook?

Server
------

Install fireball for all servers:

    $ ansible-playbook datafly/ansible/fireball.yaml

Setup fireball connection for 30 minutes:

    $ ansible-playbook script/fireball.yaml

From Ansible documentation:

> Fireball mode works by launching a temporary 0mq daemon from SSH that by
default lives for only 30 minutes before shutting off.

You are ready to install and launch Nginx, uWSGI:

    $ ansible-playbook script/server.yaml

