DataFly Starter
===============

Please read [Requirements](/requirements) page first.

Download
--------

Open your main projects folder or special folder for DataFly projects.

To install or update simply use Git:

```bash
  $ cd /home/user/projects
  $ git clone git@bitbucket.org:df-sean/datafly-starter.git
```

How to use
----------

Starter is used as a base for development (no need to upload to remote server or
install as package).

Current structure:

```bash
  /datafly-starter  
  -/doc # Documentation website (and Markdown source files)
  -/new_project # New project boilerplate, copy & make "initial commit"
  # tools to deploy project (Fabric & Ansible scripts)
  --/script
  ---/datafly # code from this folder is reused for all projects
  ---fabfile.py
  ---hosts
  ---devops.yaml
  # requirements.txt, Nginx and uWSGI configuration files
  --/server
  # models, views, templates
  --/www
  ---/datafly # code from this folder is reused for all projects
  ---/less
  ---/js
  ---/static # served by Nginx as static files (/static/<file_path>)
  ----/compiled # combined, minified CSS & JS files
  ---/models
  ---/templates
  ---/views
  ---app.py  
```

