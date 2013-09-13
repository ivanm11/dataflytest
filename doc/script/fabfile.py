import sys
from os import pardir
from os.path import abspath, join, dirname

from fabric.api import env

# path to DataFly Fabric core
sys.path.append(join(pardir, pardir, 'new_project', 'script'))

# set project root for imported commands
env.PROJECT_ROOT = abspath(join(dirname(__file__), pardir))

from datafly.fabric.core import *