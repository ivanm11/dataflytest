import sys
from os.path import abspath, dirname

from fabric.api import env

env.root_dir = abspath(dirname(dirname(__file__)))
sys.path.append(env.root_dir)

# edit env vars before using deploy, git_init commands
env.project  = 'newproject'
env.remote_path = '/home/newproject/'
env.hosts = ['staging.newproject.com']
env.user  = 'root'

from datafly.fabric.fabfile import deploy, git, repo