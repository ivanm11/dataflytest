import os
from os.path import abspath, join, dirname

# extend your application with custom Jinja2 filters
from jinja2_ext import extended_filters

# SITE ROOT - /www
SITE_ROOT = abspath(dirname(__file__))
# one level above site
PROJECT_ROOT = abspath(join(SITE_ROOT, '..'))

class Default(object):
    DB = 'newproject'
    CACHE_TIMESTAMP = 'June30_2013_2100' 
    DEVOPS_CONFIG = 'devops.yaml'
    SECRET = 'EJdDcCRXHTyW8UXcQnRhWyujGWnK7Bjf4ZD68ve9Heu9tvCwacPc9zYjwJrb'
    MONGO = {
        'host': 'localhost',
        'port': 27017
    }

class Production(Default):
    BASE_URL = 'http://newproject.com'

class Staging(Default):
    BASE_URL = 'http://staging.newproject.com'

"""
    please, define class Development(Default) in myconfig.py
    with your local settings    

    myconfig.py file is not versioned by Git, however
    add a copy of yours as myconfig_name.py to Git
    (or better add a symlink `ln -s myconfig.py myconfig_name.py`)
"""

# environ variable is defined in project.ini uWSGI configuration file
config_name = os.environ.get('CONFIG', False)
if config_name:
    # Config = Production or Config = Staging
    Config = vars()[config_name]
else:          
    import myconfig
    Config = myconfig.Development