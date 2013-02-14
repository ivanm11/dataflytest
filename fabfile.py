from os import path

import yaml

from fabric.api import env
# local
from fabric.api import lcd, local
# server
from fabric.api import run

# Folders

root_dir = path.abspath(path.dirname(path.dirname(__file__)))
www_dir = path.join(root_dir, 'www')
server_dir = path.join(root_dir, 'server')
datafly_dir = path.join(root_dir, 'datafly')

# Parse YAML

config_file = path.join(root_dir, 'config.yaml')
config = yaml.load(open(config_file))

# Remote configration

env.user = config['server']['user']
env.hosts = config['server']['hosts']

def _replace_in_file(path, replacements):
    source = open(path).read()
    for key, value in replacements.iteritems():
        var = '{{ $%s }}' % key
        source = source.replace(var, str(value))
    output = open(path, 'w')
    output.write(source)
    output.close

# INSTALLATION AND MAINTENANCE

def new_project(action=None):
    def copy_files():
        files = path.join(datafly_dir, config['project']['type'], '*')
        local('cp -r %s %s' % (files, root_dir))
    def setup_venv():
        with lcd(root_dir):
            local('virtualenv venv')
            local('venv/bin/pip install -r server/requirements.txt')
            local('mkdir -p backup')
    if action:
        return locals()[action]()
    copy_files()
    setup_venv()


uwsgi_filename = '%s.ini' % config['project']['name']
nginx_filename = '%s.nginx' % config['project']['name']

def conf():
    if config['server']['type'] == 'nginx_uwsgi':
        files = path.join(datafly_dir, 'nginx_uwsgi', '*')
        local('cp -r %s %s' % (files, server_dir))
        with lcd(path.join(root_dir, 'server')):
            # uwsgi conf
            local('mv uwsgi.ini %s' % uwsgi_filename)
            uwsgi_path = path.join(server_dir, uwsgi_filename)
            _replace_in_file(uwsgi_path, config['server']['uwsgi'])
            # nginx conf
            local('mv default.nginx %s' % nginx_filename)
            nginx_path = path.join(server_dir, nginx_filename)
            _replace_in_file(nginx_path, config['server']['nginx'])


def server(action=None):
    """Only Ubuntu & Debian"""
    if action == 'install' and config['server']['type'] == 'nginx_uwsgi':
        run('apt-get install nginx')
        run('apt-get install build-essential python-dev libxml2-dev')
        run('apt-get install python-pip')
        run('pip install uwsgi')
    if action == 'configure' and config['server']['type'] == 'nginx_uwsgi':
        remote_server_dir = path.join(config['server']['path'], 'server')
        remote_nginx_conf = path.join(remote_server_dir, uwsgi_filename)
        run('ln -s %s /etc/nginx/sites-enabled/%s'
            % (remote_nginx_conf, uwsgi_filename))
        run('service nginx reload')
        remote_uwsgi_conf = path.join(remote_server_dir, nginx_filename)
        run('ln -s %s /etc/uwsgi/vassals/%s'
            % (remote_uwsgi_conf, nginx_filename))


def compile_docs():
    with lcd(datafly_dir):
        local('markdown2 docs.md > docs.html')


# SHARED METHODS

def bottle_run():
    with lcd(www_dir):
        local('../venv/bin/python app.py')