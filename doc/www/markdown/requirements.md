Requirements
============

Install *pip* and then *fabric*, *virtualenv* packages globally using *pip*.

Requirements.txt
----------------

List of required packages for a project - `server/requirements.txt`.

To get a nice output for currently installed packages use:

```bash
  # run from virtualenv
  pip freeze -r requirements.txt > freeze.txt
```

Pillow
------

[Pillow documentation: Installation.](http://pillow.readthedocs.org/en/latest/installation.htm)

*Ubuntu*

```bash
    $ sudo apt-get install python-dev python-setuptools
    $ sudo apt-get install libtiff4-dev libjpeg8-dev zlib1g-dev
```

*Mac OS X*

You’ll need XCode to install Pillow. (XCode 4.2 on 10.6 will work with the
Official Python binary distribution. Otherwise, use whatever XCode you used
to compile Python.)

```bash
    $ brew install libtiff libjpeg webp littlecms
```

LESS compiler
-------------

[LESS documentation](http://lesscss.org/#docs)

Node.js required. Install with [npm](https://npmjs.org/):

```bash
  $ sudo npm install -g less
```

`fab collect_static` command is using LESS compiler.

MongoDB
-------

Install latest stable release of MongoDB.

For Ubuntu you have to add MongoDB downloads repository and install *mongodb-10gen*
package. Although Ubuntu does include MongoDB packages, the official
packages are generally more up to date.

*Robomongo*

Shell-centric application, very useful to inspect current databases and collections:

[http://robomongo.org/](http://robomongo.org/)

Ansible (MacOSX / Linux only)
-----------------------------

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