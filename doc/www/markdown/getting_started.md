GETTING STARTED
===============

Introduction
------------

We start with a minimum amount of code and use modern tools for deployment and
client-side coding. NoSQL and No Big and Heavy Framework. This approach should
help us make custom projects fast and easily maintain them afterwards.

Tools we use
------------

*Framework*

[Bottle Microframework](http://bottle.readthedocs.org/en/release-0.11/)
(latest stable) with [Jinja 2](http://jinja.pocoo.org/docs/)

[MongoDB](http://docs.mongodb.org/manual/)
(latest stable)

[PyMongo](http://api.mongodb.org/python/current/)
(and our tiny single-file Object Document Mapper module)

[DataFly Starter](/datafly-starter)
(new project boilerplate, Fabric & Ansible global scripts)

*Environment/revision control*

[Virtualenv](http://www.virtualenv.org/en/latest)
(please, no `--system-site-packages`)

[Git](http://gitref.org/index.html)

*DevOps*

[Fabric](http://docs.fabfile.org/en/1.6/)
(deployment commands)

[Ansible](http://www.ansibleworks.com/docs/gettingstarted.html)
(to manage server configuration)

*Server*

[Nginx](http://wiki.nginx.org/Main)
(latest stable)

[uWSGI](http://uwsgi-docs.readthedocs.org/en/latest/)
(latest stable, Emperor Mode)

Important resources
-------------------

General Documentation ("authorize me" link)  
[http://doc.datafly.net/?password=WeL1C00Me](http://doc.datafly.net/?password=WeL1C00Me)  

Project Management  
[ProjectSputnik](http://datafly.projectsputnik.com)

Fabric and Ansible helpers, New Project boilerplate  
`git@bitbucket.org:df-sean/datafly-starter.git`

Latest approach / structure of a simple project with Dashboard  
`git@bitbucket.org:df-sean/datafly-starter.git/new_project`  
[http://starter.datafly.net/section/page](http://starter.datafly.net/section/page)  
[http://starter.datafly.net/admin/login](http://starter.datafly.net/admin/login)

Dashboard:  
email - *demo@datafly.net*, password - *demo*.

Script House - good example of a project without Dashboard, fat model classes
`git@bitbucket.org:df-sean/script-house.git`

This documentation website - ways to minimize application
`git@bitbucket.org:df-sean/datafly-starter.git/doc`