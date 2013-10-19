DataFly Starter
===============

Download
--------

Open your projects home folder or special folder for DataFly projects.

To install & update we simply using Git:

```bash
  $ cd /home/user/projects
  $ git clone git@bitbucket.org:df-sean/datafly-starter.git
```

How to use
----------

DataFly Starter should be placed somewhere outside of your new/existing project
folder.

Starter is used for development only (no need to upload to remote or
install as package).

Current structure, contains four components (root folders):

```bash
  /starter
  --/new_project # New project bootstrap
  ----/www
  ------/datafly # code from this folder is reused for all projects
  ------/static # full set of HTML, JS libs we use frequently
  --/doc # Documentation website (and Markdown files)
```

Please install Fabric, Ansible, Virtualenv.

More info on Ansible install in section *How to install Ansible*.

Always go to `script` dir to run Fabric tasks.

How to install Ansible
----------------------

Please install latest Ansible and all required dependencies
globally:

```bash
  $ sudo pip install paramiko PyYAML jinja2 ansible --upgrade
```

This is required for Ansible Accelerate mode:

```bash
  $ sudo pip install python-keyczar
```

From Ansible documentation:

> Accelerated mode can be anywhere from 2-6x faster than SSH with ControlPersist
enabled, and 10x faster than paramiko.