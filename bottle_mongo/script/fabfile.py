import sys
from os.path import abspath, dirname

project_path = abspath(dirname(dirname(__file__)))
sys.path.append(project_path)

# run()
from datafly.fabfile import bottle_run as run

