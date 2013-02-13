import os.path
from os.path import abspath, dirname

import yaml

from fabric.api import env
# local
from fabric.api import lcd, local
# server
from fabric.api import run

# /projects/new_project
project_path = abspath(dirname(dirname(__file__)))
www_path = os.path.join(project_path, 'www')
server_path = os.path.join(project_path, 'server')
# /projects/new_project/datafly
datafly_path = abspath(dirname(__file__))

config_file = os.path.join(project_path, 'config.yaml')
config = yaml.load(open(config_file))

env.user = config['server']['user']
env.hosts = config['server']['hosts']

def _replace_in_file(path, replacements):
    source = open(path).read()
    for k, v in replacements.iteritems():
        source = source.replace('{{ $%s }}' % k, v)
    output = open(path, 'w')
    output.write(source)
    output.close

# INSTALLATION AND MAINTENANCE

def server_setup():
    """Only Ubuntu & Debian"""
    run('apt-get install nginx')
    run('apt-get install build-essential python-dev libxml2-dev')
    run('apt-get install python-pip')
    run('pip install uwsgi')

uwsgi_conf = '%s.ini' % config['project']['name']
nginx_conf = '%s.nginx' % config['project']['name']

def starter_install():
    files = os.path.join(datafly_path, config['project']['type'], '*')
    local('cp -r %s %s' % (files, project_path))
    with lcd(os.path.join(project_path, 'server')):
        local('mv uwsgi.ini %s' % uwsgi_conf)
        path = os.path.join(server_path, uwsgi_conf)
        # _replace_in_file(path, config['server']['uwsgi'])
        local('mv vhost.nginx %s' % nginx_conf)
        path = os.path.join(server_path, nginx_conf)
        # _replace_in_file(path, config['server']['nginx'])

def starter_deploy():
    remote_server_path = os.path.join(config['server']['path'], 'server')
    nginx_conf_fullpath = os.path.join(remote_server_path, nginx_conf)
    run('ln -s %s /etc/nginx/sites-enabled/%s' % (nginx_conf_fullpath, nginx_conf))
    run('service nginx reload')
    uwsgi_conf_fullpath = os.path.join(remote_server_path, uwsgi_conf)
    run('ln -s %s /etc/uwsgi/vassals/%s' % (uwsgi_conf_fullpath, uwsgi_conf))

def local_setup():
    with lcd(project_path):
        # local('virtualenv venv')
        local('venv/bin/pip install -r server/requirements.txt')
        local('mkdir backup')

def compile_docs():
    with lcd(datafly_path):
        local('markdown2 docs.md > docs.html')

# SHARED METHODS

def bottle_run():
    with lcd(www_path):
        local('../venv/bin/python app.py')