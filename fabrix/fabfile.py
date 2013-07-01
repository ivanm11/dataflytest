import sys, yaml
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
    sys.path.append(SITE_ROOT)
    # project specific variables from yaml
    stream = file(path.join(SITE_ROOT, 'devops.yaml'), 'r')
    devops = yaml.load(stream)
    env.hosts = devops['server']

@task
def venv():
    """ Install virtualenv or update packages from requirements.txt """
    with lcd(PROJECT_ROOT):
        if not path.exists(path.join(PROJECT_ROOT, 'venv')):
            local('virtualenv venv')
            local('source venv/bin/activate')
        local('venv/bin/pip install -r server/requirements.txt')               

@task
def app_run():
    """ Run development server """
    with lcd(SITE_ROOT):
        local('python app.py')

# DEPLOY

@task
def mkdir(version=None):
    REMOTE_PATH = path.join(devops['remote_path'] + version)
    run('mkdir -p %s/www' % REMOTE_PATH)
    run('mkdir -p %s/backup' % REMOTE_PATH)
    run('mkdir -p %s/server' % REMOTE_PATH)
    return REMOTE_PATH  

@task
def chmod(version=None):
    REMOTE_PATH = path.join(devops['remote_path'] + version)
    run('chown -R www-data:www-data %s/www' % REMOTE_PATH)
    run('mkdir -p %s/www/static/upload/img' % REMOTE_PATH)    
    run('chmod -R 775 %s/www/static/upload/img' % REMOTE_PATH)
    run('mkdir -p %s/www/static/upload/file' % REMOTE_PATH)
    run('chmod -R 775 %s/www/static/upload/file' % REMOTE_PATH)

@task
def deploy(version=None):
    REMOTE_PATH = path.join(devops['remote_path'] + version)
    mkdir(version)
    # version - production or staging
    requirements = '%s/server/requirements.txt'
    put(requirements % PROJECT_ROOT, requirements % REMOTE_PATH)
    rsync_project('%s/' % REMOTE_PATH, SITE_ROOT, exclude=["*.pyc"])
    venv_remote(REMOTE_PATH)
    with cd(REMOTE_PATH):
        run('venv/bin/pip install -r server/requirements.txt')
        run("find . -name '*.pyc' -delete")
    chmod(version)
    run('service uwsgi restart')

def venv_remote(remote_path):
    if not files.exists('%s/venv' % remote_path):
        run('apt-get install python-pip')
        run('apt-get install rsync')
        run('pip install virtualenv')
        run('virtualenv %s/venv' % remote_path)

def put_images(version):
    remote_path = env.remote_path + version
    remote_images = path.join(remote_path, 'www', 'static', 'img', 'upload')
    local_images = path.join(env.root_dir, 'www', 'static', 'img', 'upload', '*')
    run('chmod -R 775 %s/www/static/img/upload' % remote_path)
    put(local_images, remote_images)

def get_db():
    run('rm -rf /tmp/%s' % env.db)
    run('mongodump --db %s --out /tmp' % env.db)
    filename = '%s.tar.gz' % strftime("%d%b%Y%H%M", gmtime())
    run('tar -zcf /tmp/%s /tmp/%s' % (filename, env.db))
    get('/tmp/%s' % filename, path.join(env.root_dir, 'backup'))
    with lcd(path.join(env.root_dir, 'backup')):
        local('tar -xvf %s' % filename)
    restore_from = path.join(env.root_dir, 'backup', 'tmp', env.db)
    local('mongorestore --drop --db %s %s' % (env.db, restore_from))

def put_db(version):
    remote_path = env.remote_path + version
    local('rm -rf /tmp/%s' % env.db)
    local('mongodump --db %s --out /tmp' % env.db)
    filename = '%s.tar.gz' % strftime("%d%b%Y%H%M", gmtime())
    local('tar -zcf /tmp/%s /tmp/%s' % (filename, env.db))
    put('/tmp/%s' % filename, path.join(remote_path, 'backup'))
    with cd(path.join(remote_path, 'backup')):
        run('tar -xvf %s' % filename)
    restore_from = path.join(remote_path, 'backup', 'tmp', env.db)
    run('mongorestore --drop --db %s %s' % (env.db, restore_from))

# INSTALLATION

@task
def git():
    env.hosts = ['root@datafly.net']

@task
def repo():
    repository = '/home/git/%s.git' % devops['project']
    #run('mkdir %s' % repository)
    with cd(repository):
        run('git init --bare')
        run('chown -R git:git .')
    with lcd(PROJECT_ROOT):
        local('git init')
        local('git add .')
        local('git commit -m "Initial commit"')
        local('git checkout -b staging')
        remote_origin = 'ssh://git@datafly.net%s' % repository
        local('git remote add origin %s' % remote_origin)
        local('git push origin master')
        local('git push origin staging')

@task
def collect_static():
    """ Needs refactoring. Append files into groups, compile if LESS"""
    STATIC_ROOT = path.join(SITE_ROOT, 'static')
    # LESS
    for result in devops['less']:
        output_less = path.join(STATIC_ROOT, '%s.less' % result)        
        output_less = open(output_less, 'w')     
        for file in devops['less'][result]:
            less = path.join(SITE_ROOT, file+'.less')
            file = open(less, 'r')
            output_less.write(file.read())
        output_less.close()
        local('lessc %s/%s.less -o %s/%s.min.css' % (STATIC_ROOT, result, STATIC_ROOT, result))
    # JS
    for result in devops['js']:        
        output_js = path.join(STATIC_ROOT, '%s.min.js' % result)
        output_js = open(output_js, 'w')     
        for file in devops['js'][result]:
            js = path.join(SITE_ROOT, file+'.js')
            file = open(js, 'r')
            output_js.write(file.read())
        output_js.close()
    

# ultimate shortcut for deploy:staging
def d():
    collect_static()
    put_db('staging')
    deploy('staging')