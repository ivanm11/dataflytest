import os
from os.path import abspath, join, dirname

CONFIG_ROOT = abspath(dirname(__file__))
# SITE ROOT - /www
SITE_ROOT = abspath(join(CONFIG_ROOT, '..'))
# one level above site
PROJECT_ROOT = abspath(join(SITE_ROOT, '..'))

class Default(object):
    CACHE_TIMESTAMP = 'Sep14-0225' 
    WEBSITE = 'DataFly'    
    MONGO = {
        'host': 'localhost',
        'port': 27017        
    }
    ADMIN_USER = {
        'login': 'demo@datafly.net',
        'password': 'demo'
    }   
    DB = 'starter'
    IMG_PREFIX = ''
    SECRET = 'EJdDcCRXHTyW8UXcQnRhWyujGWnK7Bjf4ZD68ve9Heu9tvCwacPc9zYjwJrb'

class Production(Default):
    BASE_URL = 'http://starter.datafly.net'

class Staging(Default):
    BASE_URL = 'http://staging.starter.datafly.net'

class Development(Default):
    BASE_URL = 'http://127.0.0.1:8080'
    HOST = '127.0.0.1'
    PORT = 8080    
    LESSJS = False

"""
    please, define class Development(Default) in myconfig.py
    with your local settings    

    myconfig.py file is not versioned by Git, however
    add a copy of yours as myconfig_name.py to Git
    (or better add a symlink `ln -s myconfig.py myconfig_name.py`)
"""

# environ variable is defined in uwsgi.ini uWSGI configuration file
config_name = os.environ.get('CONFIG', False)
if config_name:
    # Config = Production or Config = Staging
    Config = vars()[config_name]
else:        
    try:  
        import myconfig
        Config = myconfig.Development
    except ImportError:
        Config = Development