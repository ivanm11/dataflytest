import sys
from os.path import abspath, dirname

project_path = abspath(dirname(dirname(__file__)))
sys.path.append(project_path)

from datafly.fabfile import root_dir, www_dir, server_dir, datafly_dir

# run()
from datafly.fabfile import bottle_run as run

