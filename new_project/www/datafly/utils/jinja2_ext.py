import urllib
from pytz import timezone, utc
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

def strftime(value, fmt):
    pacific = timezone('US/Pacific')
    return utc.localize(value).astimezone(pacific).strftime(fmt)

filters = dict(
    urlencode = urlencode_filter,
    getkey = getkey,
    money = money,
    to_json = json.dumps,
    from_json = json.loads,
    strftime = strftime
)

_globals = dict()

