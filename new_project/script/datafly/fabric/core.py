import os, sys, yaml
from os import path
from time import strftime, gmtime

# local
from fabric.api import lcd, local, get
# server
from fabric.api import cd, run, put
# other
from fabric.api import env, task
from fabric.contrib import files
from fabric.contrib.project import rsync_project

# env.PROJECT_ROOT - that's all we know
if hasattr(env, 'PROJECT_ROOT'):
    # SITE ROOT - /www
    PROJECT_ROOT = env.PROJECT_ROOT
    SITE_ROOT = path.abspath(path.join(env.PROJECT_ROOT, 'www'))
    STATIC_ROOT = path.join(SITE_ROOT, 'static')
    sys.path.append(SITE_ROOT)
    try:
        from config import config, assets
    except ImportError:
        import config
    CONFIG = {
        'default': config.Default,
        'production': getattr(config, 'Production', None),
        'staging': getattr(config, 'Staging', None)
    }
    # project specific variables from yaml
    stream = file(path.join(PROJECT_ROOT, 'script', 'devops.yaml'), 'r')
    DEVOPS = yaml.load(stream)
    env.hosts = DEVOPS['hosts']

@task
def ansible(playbook): 
    """ Ansible shortcut """
    local('ansible-playbook %s.yaml -i hosts' % playbook)

@task
def venv():
    """ Install virtualenv or update packages from requirements.txt """
    with lcd(PROJECT_ROOT):
        if not path.exists(path.join(PROJECT_ROOT, 'venv')):
            local('virtualenv venv')
        local('venv/bin/pip install -r server/requirements.txt')       

@task
def devenv():
    """ My favourite development tools for Python """
    with lcd(PROJECT_ROOT):
        local('venv/bin/pip install pudb bpython chromelogger')

@task
def checkout(branch):    
    local('git checkout %s' % branch)
    local("find . -name '*.pyc' -delete")

@task
def runserver():
    """ Run development server """
    with lcd(SITE_ROOT):
        local('../venv/bin/python app.py')

# DEPLOY

@task
def mkdir(version=None):
    REMOTE_PATH = path.join(DEVOPS['remote_path'], version)
    run('mkdir -p %s/www' % REMOTE_PATH)
    run('mkdir -p %s/backup' % REMOTE_PATH)
    run('mkdir -p %s/server' % REMOTE_PATH)
    return REMOTE_PATH  

@task
def remote_venv(remote_path):
    if not files.exists('%s/venv' % remote_path):
        run('apt-get install python-pip')
        run('apt-get install rsync')
        run('pip install virtualenv')
        run('virtualenv %s/venv' % remote_path)

@task
def chmod(version=None):
    REMOTE_PATH = path.join(DEVOPS['remote_path'], version)
    run('chown -R www-data:www-data %s/www' % REMOTE_PATH)
    run('mkdir -p %s/www/static/upload/img' % REMOTE_PATH)    
    run('chmod -R 775 %s/www/static/upload/img' % REMOTE_PATH)
    run('mkdir -p %s/www/static/upload/file' % REMOTE_PATH)
    run('chmod -R 775 %s/www/static/upload/file' % REMOTE_PATH)

@task
def deploy(version=None, fast=False, delete=False):
    REMOTE_PATH = path.join(DEVOPS['remote_path'], version)
    if not fast:
        mkdir(version)
        # version - production or staging
        requirements = '%s/server/requirements.txt'
        put(requirements % PROJECT_ROOT, requirements % REMOTE_PATH)
    delete = True if version == 'staging' or delete else False
    rsync_project('%s/' % REMOTE_PATH, SITE_ROOT,
                  delete=delete, exclude=["*.pyc", "upload"])    
    if not fast:
        remote_venv(REMOTE_PATH)
        with cd(REMOTE_PATH):
            run('apt-get install libxml2-dev libxslt1-dev')
            run('venv/bin/pip install -r server/requirements.txt')
            run("find . -name '*.pyc' -delete")    
        chmod(version)
    run('service uwsgi restart')

@task
def backup_db(version):
    db = CONFIG[version].DB
    run('rm -rf /tmp/%s' % db)
    run('mongodump --db %s --out /tmp' % db)
    id = db + '_' + strftime("%d%b%Y%H%M", gmtime())
    filename = '%s.tar.gz' % id
    with cd('/tmp'):
        run('tar -zcf %s %s' % (filename, db))
    backup_dir = path.join(PROJECT_ROOT, 'backup')
    get('/tmp/%s' % filename, backup_dir)
    if os.name == 'posix':        
        with lcd(backup_dir):            
            local('rm -rf %s' % db)
            local('tar xvf %s' % filename)

@task
def get_db(version):
    db = CONFIG[version].DB  
    backup_db(version)
    restore_from = path.abspath(path.join(PROJECT_ROOT, 'backup', db))
    local('mongorestore --drop --db %s %s' % (db, restore_from))

@task
def get_upload(version):
    REMOTE_PATH = path.join(DEVOPS['remote_path'], version)
    remote_upload = path.join(REMOTE_PATH, 'www', 'static', 'upload')
    local_upload = path.join(STATIC_ROOT, 'upload')
    rsync_project(remote_upload, local_upload, upload=True)

@task
def migration(version, file=None):
    REMOTE_PATH = path.join(DEVOPS['remote_path'], version)
    MIGRATIONS = path.join(PROJECT_ROOT, 'script', 'migrations')
    rsync_project('%s/script/' % REMOTE_PATH, MIGRATIONS, exclude=["*.pyc"])
    if file:
        with cd(REMOTE_PATH):
            run('venv/bin/python script/migrations/%s %s' % (file, version))

@task
def put_db(version):
    db = CONFIG[version].DB
    local('rm -rf /tmp/%s' % db)
    local('mongodump --db %s --out /tmp' % db)
    id = db + '_' + strftime("%d%b%Y%H%M", gmtime())
    filename = '%s.tar.gz' % id
    with lcd('/tmp'):
        local('tar -zcf %s %s' % (filename, db))
    put('/tmp/%s' % filename, '/tmp/%s' % filename)
    run('''mongo --eval "db.copyDatabase('%s','%s_tmp')"''' % (db, db))
    run('rm -rf /tmp/%s' % db)    
    with cd('/tmp'):
        run('tar -xvf %s' % filename)
        run('mongorestore --drop --db %s %s' % (db, db))

# INSTALLATION

@task
def collect_static():
    """ Needs refactoring. Append files into groups, compile if Less. """    
    # LESS
    for result in assets.LESS:
        output_less = path.join(SITE_ROOT, 'less', '%s.tmp.less' % result)
        output_less = open(output_less, 'w')
        for file in assets.LESS[result]:
            less = path.join(SITE_ROOT, file+'.less')
            file = open(less, 'r')
            output_less.write(file.read())
        output_less.close()
        local('lessc %s/less/%s.tmp.less -o %s/%s.min.css' % (SITE_ROOT, result, STATIC_ROOT, result))
    # JS
    for result in assets.JS:
        output_js = path.join(STATIC_ROOT, '%s.min.js' % result)
        output_js = open(output_js, 'w')
        for file in assets.JS[result]:
            js = path.join(SITE_ROOT, file+'.js')
            file = open(js, 'r')
            output_js.write(file.read())
        output_js.close()

@task
def ds():
    """ shortcut for deploy:staging """
    collect_static()
    deploy('staging', fast=True)

@task
def dp():
    """ shortcut for deploy:production """
    collect_static()
    deploy('production', fast=True)