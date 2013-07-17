import os
from os.path import abspath, join, dirname

# SITE ROOT - /www
SITE_ROOT = abspath(dirname(__file__))
# one level above site
PROJECT_ROOT = abspath(join(SITE_ROOT, '..'))

class Default(object):
    CACHE_TIMESTAMP = 'July17_2013_0533' 
    WEBSITE = 'Documentation / Datafly'    
    # STATIC ASSETS
    # TYPE = { result: [files] }
    # files - list of files to compile, concat, minify (relative to /www directory)
    LESS = {
        'public': [
            'datafly/admin/layout',
            'less/docs'        
        ]
    }
    JS = {
        'public': []
    }
    PASSWORD = 'WeL1C00Me'
    SECRET = 'VGRxWrQ[,;6><lw3[lGs8etxsB{r)rlW6b]db|Y-Jz~paTEB2'

class Production(Default):
    pass

class Development(Default):
    pass
    HOST = '127.0.0.1'
    PORT = 9080    

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