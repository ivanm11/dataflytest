from os import path

# local
from fabric.api import lcd, local
# server
from fabric.api import cd, run, put
# other
from fabric.api import env
from fabric.contrib import files
from fabric.contrib.project import rsync_project

# Local directories

if hasattr(env, 'root_dir'):
    # datafly folder is a symlink inside project folder
    root_dir = path.abspath(path.dirname(path.dirname(env.root_dir)))
else:
    root_dir = path.abspath(path.dirname(path.dirname(path.dirname(__file__))))

datafly_dir = path.join(root_dir, 'datafly')

# DEPLOY

def deploy(version):
    # version - production or staging
    remote_path = env.remote_path + version
    run('mkdir -p %s/www' % remote_path)
    run('mkdir -p %s/server' % remote_path)
    if not files.exists('%s/venv' % remote_path):
        run('apt-get install python-pip')
        run('pip install virtualenv')
        run('virtualenv %s/venv' % remote_path)
    template = '%s/server/requirements.txt'
    put(template % env.root_dir, template % remote_path)
    rsync_project('%s/www/' % remote_path, '%s/www/' % env.root_dir)
    with cd(remote_path):
        run('venv/bin/pip install -r server/requirements.txt')
    run('chown www-data:www-data %s/www' % remote_path)
    run('service uwsgi restart')

# INSTALLATION

def new(project_type):
    this_project = path.join(datafly_dir, project_type, '.')
    local('cp -r %s %s' % (this_project, root_dir))
    with lcd(root_dir):
        local('virtualenv venv')
        local('venv/bin/pip install -r server/requirements.txt')
        local('mkdir -p backup')

def git():
    env.hosts = ['96.126.102.11']

def repo():
    repository = '/home/datafly/git/%s.git' % env.project
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
        run('chown -R datafly:datafly .')

def docs():
    with lcd(datafly_dir):
        local('markdown2 docs/docs.md > docs/docs.html')

# DEPRECATED! Replaced with Ansible playbooks
def new_server(action=None):
    """Only Ubuntu & Debian
    if action == 'install' and server['type'] == 'nginx_uwsgi':
        run('apt-get install nginx')
        run('apt-get install build-essential python-dev libxml2-dev')
        run('apt-get install python-pip')
        run('pip install uwsgi')
        run('service nginx start')
        run('mkdir /etc/uwsgi && mkdir /etc/uwsgi/vassals')
        put(path.join(datafly_dir, 'nginx_uwsgi', 'uwsgi.conf'), '/etc/init/')
        run('service uwsgi start')
    if action == 'configure' and server['type'] == 'nginx_uwsgi':
        # TODO: staging
        if production['update'] == 'git':
            run('git clone %s %s' % (repository['path'], production['path']))
        with cd(production['path']):
            run('virtualenv venv')
            run('venv/bin/pip install -r server/requirements.txt')
        remote_server_dir = path.join(production['path'], 'server')
        remote_nginx_conf = path.join(remote_server_dir, nginx_site)
        run('ln -s %s /etc/nginx/sites-enabled/%s'
            % (remote_nginx_conf, nginx_site))
        run('service nginx reload')
        remote_uwsgi_conf = path.join(remote_server_dir, uwsgi_ini)
        run('ln -s %s /etc/uwsgi/vassals/%s'
            % (remote_uwsgi_conf, uwsgi_ini))
    """
    pass