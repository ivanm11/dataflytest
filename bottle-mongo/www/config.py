import os
from os import path

_root_dir = path.abspath(path.dirname(__file__))

class Default(object):
    CACHE_TIMESTAMP = 'May01_2013_2335'
    ADMIN_USER = {
        'login': '',
        'password': ''
    }
    SECRET = 'Rsh+zX#crk8A9!%_W\-bq`G:|GXCI]p0P0Xt*UD1n:8+/(`2j'
    APPS = ['admin', 'pages']
    PAGES_BACKEND = 'mongo'

class Production(Default):
    pass

class Staging(Default):
    pass

class Development(Default):
    pass

config = None

if config is None:
    ConfigEnv = os.environ.get('Config', 'Development')
    Config = globals()[ConfigEnv]