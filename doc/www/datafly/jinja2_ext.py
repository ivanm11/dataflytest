import urllib
from os.path import basename, normpath
from operator import getitem
from jinja2 import Markup

try:
    import json
except ImportError:
    import simplejson as json

def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.quote_plus(s)
    return Markup(s)

def getkey(d, key):
    try:
        return reduce(getitem, key.split("."), d)
    except (KeyError, TypeError):
        return ""

def money(value, usd=True, roundup=False):
    value = int(value / 100.00) + 1 if roundup else value / 100.00
    with_cents = '{:.2f}'.format(value)
    return '$' + with_cents if usd else with_cents

filters = dict(
    urlencode = urlencode_filter,
    getkey = getkey,
    money = money,
    to_json = json.dumps,
    from_json = json.loads
)

def get_static_path(assets_path, ext):
    """ convert assets.py path to /static/compiled """
    if 'less' in assets_path:
        return '/static/compiled/%s.css' % basename(normpath(assets_path))
    if 'coffee' in assets_path:
        return '/static/compiled/%s.js' % basename(normpath(assets_path))
    return '/%s.%s' % (assets_path, ext)

_globals = dict(
    get_static_path = get_static_path
)