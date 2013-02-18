from os import path

import yaml

# local
from fabric.api import lcd, local
# server
from fabric.api import cd, run, put, env, hosts

from helpers import rename_and_replace_in_file

# Local directories

root_dir = path.abspath(path.dirname(path.dirname(__file__)))
www_dir = path.join(root_dir, 'www')
server_dir = path.join(root_dir, 'server')
datafly_dir = path.join(root_dir, 'datafly')

# Parse YAML

config_file = path.join(root_dir, 'config.yaml')
config = yaml.load(open(config_file))

project = config['project']
server = config.get('server', None)
repository = config['repository']
production = config['production']
staging = config.get('staging', None)

# if single user/host pair for all env
for conf in (repository, production, staging):
    if conf and 'user' not in conf:
        conf['hosts'] = server['hosts']
        conf['password'] = server.get('password', None)

env.hosts = staging['hosts'] if staging else production['hosts']

# TODO: refactoring
nginx_site = '%s.nginx' % project['name']
production['nginx']['path'] = production['path']
production['nginx']['socket'] = production['uwsgi']['socket']
nginx = {
    'source': path.join(server_dir, 'site.nginx'),
    'target': path.join(server_dir, nginx_site),
    'replacements': production['nginx']
}
uwsgi_ini = '%s.ini' % project['name']
production['uwsgi']['path'] = production['path']
uwsgi = {
    'source': path.join(server_dir, 'uwsgi.ini'),
    'target': path.join(server_dir, uwsgi_ini),
    'replacements': production['uwsgi']
}

if staging:
    nginx_staging_site = '%s_staging.nginx' % project['name']
    staging['nginx']['path'] = staging['path']
    staging['nginx']['socket'] = staging['uwsgi']['socket']
    nginx_staging = {
        'source': path.join(server_dir, 'site_staging.nginx'),
        'target': path.join(server_dir, nginx_staging_site),
        'replacements': staging['nginx']
    }
    uwsgi_staging_ini = '%s_staging.ini' % project['name']
    staging['uwsgi']['path'] = staging['path']
    uwsgi_staging = {
        'source': path.join(server_dir, 'uwsgi_staging.ini'),
        'target': path.join(server_dir, uwsgi_staging_ini),
        'replacements': staging['uwsgi']
    }


# INSTALLATION AND MAINTENANCE

@hosts(repository['hosts'])
def new_project(action=None):
    def copy_files():
        all_projects = path.join(datafly_dir, 'all_projects', '.')
        local('cp -r %s %s' % (all_projects, root_dir))
        this_project = path.join(datafly_dir, project['type'], '.')
        local('cp -r %s %s' % (this_project, root_dir))
    def venv():
        with lcd(root_dir):
            local('virtualenv venv')
            local('venv/bin/pip install -r server/requirements.txt')
            local('mkdir -p backup')
    def conf():
        if server['type'] == 'nginx_uwsgi':
            files = path.join(datafly_dir, 'nginx_uwsgi', '.')
            local('cp -r %s %s' % (files, server_dir))
            rename_and_replace_in_file(**uwsgi)
            rename_and_replace_in_file(**nginx)
            if staging:
                rename_and_replace_in_file(**uwsgi_staging)
                rename_and_replace_in_file(**nginx_staging)
    def git_init():
        run('mkdir %s' % repository['path'])
        with cd(repository['path']):
            run('git init --bare')
        with lcd(root_dir):
            local('git init')
            local('git add .')
            local('git commit -m "Initial commit"')
            if staging:
                local('git branch staging')
            remote_origin = 'ssh://%s%s' % (repository['hosts'][0], repository['path'])
            local('git remote add origin %s' % remote_origin)
            local('git push origin master')
            if staging:
                local('git push origin staging')

    if action:
        return locals()[action]()
    copy_files()
    venv()
    conf()
    git_init()

def with_production():
    env.hosts = production['hosts']

def new_server(action=None):
    """Only Ubuntu & Debian"""
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


def compile_docs():
    with lcd(datafly_dir):
        local('markdown2 docs.md > docs.html')


# SHARED METHODS

def bottle_run():
    with lcd(www_dir):
        local('../venv/bin/python app.py')