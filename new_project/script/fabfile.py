import sys, yaml
from os.path import abspath, join, dirname

from fabric.api import env

env.PROJECT_ROOT = abspath(join(dirname(__file__), '..'))
stream = file(join(env.PROJECT_ROOT, 'script', 'mydevops.yaml'), 'r')
mydevops = yaml.load(stream)
sys.path.append(mydevops['starter'])

from fabrix.fabfile import *