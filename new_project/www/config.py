import os
from os.path import abspath, join, dirname

# SITE ROOT - /www
SITE_ROOT = abspath(dirname(__file__))
# one level above site
PROJECT_ROOT = abspath(join(SITE_ROOT, '..'))

class Default(object):
    CACHE_TIMESTAMP = 'July16_2013_2312' 
    WEBSITE = 'DataFly'    
    MONGO = {
        'host': 'localhost',
        'port': 27017        
    }
    DB = 'starter'
    # STATIC ASSETS
    # TYPE = { result: [files] }
    # files - list of files to compile, concat, minify (relative to /www directory)
    LESS = {
        'public': [
            'less/layout',
            'less/pages'        
        ],
        'admin': [
            'datafly/admin/layout'
        ]
    }
    JS = {
        'public': [
            'js/layout',
            'js/pages' 
        ],
        'admin': [
            'datafly/widgets/ajax',
            'datafly/pages/redactor',
            'datafly/users/login'
        ]
    }
    SECRET = 'EJdDcCRXHTyW8UXcQnRhWyujGWnK7Bjf4ZD68ve9Heu9tvCwacPc9zYjwJrb'

class Production(Default):
    BASE_URL = 'http://doc.datafly.net'

class Staging(Default):
    BASE_URL = 'http://staging.doc.datafly.net'

class Development(Default):
    BASE_URL = 'http://127.0.0.1:8080'
    HOST = '127.0.0.1'
    PORT = 8080    

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