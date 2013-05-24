from os import path
from time import strftime, gmtime

# local
from fabric.api import lcd, local, get
# server
from fabric.api import cd, run, put
# other
from fabric.api import env
from fabric.contrib import files
from fabric.contrib.project import rsync_project

# Local directories

if hasattr(env, 'root_dir'):
    # `/starter` folder is a symlink inside new project folder
    root_dir = path.abspath(path.dirname(path.dirname(env.root_dir)))
else:
    root_dir = path.abspath(path.dirname(path.dirname(path.dirname(__file__))))

starter_dir = path.join(root_dir, 'starter')

# DEPLOY

def deploy(version=None):
    if not version:
        print """
        Please, specify version:
        `fab deploy:staging` or `fab deploy:production`
        """
        return
    # version - production or staging
    remote_path = env.remote_path + version
    run('mkdir -p %s/www' % remote_path)
    run('mkdir -p %s/backup' % remote_path)
    run('mkdir -p %s/server' % remote_path)
    if not files.exists('%s/venv' % remote_path):
        run('apt-get install python-pip')
        run('apt-get install rsync')
        run('pip install virtualenv')
        run('virtualenv %s/venv' % remote_path)
    template = '%s/server/requirements.txt'
    put(template % env.root_dir, template % remote_path)
    rsync_project('%s/www/' % remote_path, '%s/www/' % env.root_dir)
    with cd(remote_path):
        run('venv/bin/pip install -r server/requirements.txt')
    run('chown -R www-data:www-data %s/www' % remote_path)
    run('service uwsgi restart')

def venv():
    with lcd(env.root_dir):
        local('venv/bin/pip install -r server/requirements.txt')        

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

def new(project_type):
    this_project = path.join(starter_dir, project_type, '.')
    local('cp -r %s %s' % (this_project, root_dir))
    with lcd(root_dir):
        local('virtualenv venv')
        local('venv/bin/pip install -r server/requirements.txt')
        local('mkdir -p backup')

def git():
    env.hosts = ['96.126.102.11']

def repo():
    repository = '/home/git/%s.git' % env.project
    run('mkdir %s' % repository)
    with cd(repository):
        run('git init --bare')
    with lcd(env.root_dir):
        local('git init')
        local('git add .')
        local('git commit -m "Initial commit"')
        local('git checkout -b staging')
        remote_origin = 'ssh://root@96.126.102.11%s' % repository
        local('git remote add origin %s' % remote_origin)
        local('git push origin master')
        local('git push origin staging')
    with cd(repository):
        run('chown -R git:git .')

def docs():
    with lcd(starter_dir):
        local('markdown2 docs/docs.md > docs/docs.html')