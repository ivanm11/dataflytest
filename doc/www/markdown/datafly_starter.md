DataFly Starter
===============

Download
--------

Open your projects home folder or special folder for DataFly projects.

To install & update we simply using Git:

```bash
  # password = Bbw3SIJotWhE
  $ cd /home/user/projects
  $ git clone ssh://git@datafly.net/home/git/starter.git
```

How to use
----------

DataFly Starter should live somewhere outside of your new project folder. Used
for development only (no need to upload to remote or install as package).

Current structure, contains three main components:

```bash
  /starter
  --/ansible # Ansible playbooks, see DevOps page
  --/fabrix # Fabric Extras, see DevOps page
  --/new_project # New project bootstrap
  ----/www
  ------/datafly # code from this folder is reused for all projects
  ------/static # full set of HTML, JS libs we use frequently
```

Please install Fabric, Ansible, Virtualenv.

More info on Ansible install in section `How to install Ansible`.

Always go to project `script` dir to run Fabric tasks, Ansible playbooks.

For existing project
--------------------

For existing project you can copy other developer config:

```bash
  www/myconfig_ep.py > www/myconfig.py
  www/mydevops_ep.yaml > www/mydevops.yaml # your path to project_root, starter
```

Don't forget to add your files to Git ($developer means your nickname):

```bash
  ln -s myconfig.py myconfig_$developer.py
  ln -s mydevops.yaml mydevops_$developer.yaml
```

For new project
---------------

Edit configuration files:

```bash
  www/devops.yaml # deployment information for Fabric, Ansible
  www/mydevops.yaml # path to project_root, starter
```

Add `www/mydevops.yaml` to `.gitignore`.

Create `backup` directory under project root:

```bash
  /backup
  /server
  /script
  /www
```

How to install Ansible
----------------------

Please install latest Ansible and all required dependencies
globally:

```bash
  $ sudo pip install paramiko PyYAML jinja2 ansible --upgrade
```

This is required for Ansible Fireball mode (fast connection over 0mq):

```bash
  $ sudo pip install pyzmq pyasn1 PyCrypto python-keyczar --upgrade
```

From Ansible documentation:

> Fireball mode works by launching a temporary 0mq daemon from SSH that by
default lives for only 30 minutes before shutting off.

Add servers to /etc/ansible/hosts file, example:

```ini
  [local]
  localhost

  [datafly-all]
  datafly.net
  makeastand.com
  evol.datafly.net

  [datafly]
  datafly.net

  [mas]
  makeastand.com

  [evol]
  evol.datafly.net
```



