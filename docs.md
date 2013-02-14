<title>Datafly Starter Documentation</title>
<link href="static/css/docs.css" rel="stylesheet">
<script src="http://code.jquery.com/jquery-2.0.0b1.js"></script>
<script src="static/js/docs.js"></script>

DATAFLY STARTER
===============

1. [Goals](#chapter1)
2. [Requirements](#chapter2)
3. [New Project](#chapter3)
4. [Server](#chapter4)

Goals
-----

1. Useful local & server commands for [Fabric](http://http://docs.fabfile.org/)

    1.1 Setup local and remote git repositories, add staging branch

    1.2 Install and configure nginx/uwsgi or apache/mod_wsgi

2. Start project from template (ex. *bottle_mongo*)

3. Shared python modules and css/js files between all Datafly projects.

Requirements
------------

Please, install latest versions of [Fabric](http://http://docs.fabfile.org/)
and [PyYAML](http://pyyaml.org/wiki/PyYAMLDocumentation) packages globally:

    $ sudo pip install Fabric --upgrade
    $ sudo pip install PyYAML --upgrade

If you're working on docs, install
[markdown2](https://github.com/trentm/python-markdown2) package globally:

    $ sudo pip install markdown2 --upgrade

    # compile docs with fabric
    $ fab compile_docs

New project
-----------

Make new project dir and clone datafly starter repository inside it:

    $ mkdir new_project && cd new_project
    $ git clone ssh://root@96.126.102.11/var/www/datafly.git

Copy config.example.yaml to your project folder and edit it:

    $ cp datafly/config.example.yaml config.yaml

New project based on a type in config.yaml:

    # config.yaml
    project:
        type: 'bottle_mongo'

    # shell
    $ cd datafly && fab new_project

To run using virtualenv:

    $ cd script && fab run

Server
------

Please, define your configuration in config.yaml:

    server:
        type: 'nginx_uwsgi'

To install web server run:

    $ fab server:install

To add local configuration files:

    $ fab conf

Configuration files are copied to */server* folder. You can edit them before
upload with next command.

To configure new virtual host and add wsgi configuration:

    $ fab server:configure