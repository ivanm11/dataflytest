import os, re, functools, urllib
from operator import getitem

from jinja2 import Markup
from bottle import (cached_property, HeaderDict, HeaderProperty,
                    Jinja2Template, request, response, template)

from config import Config

def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.quote_plus(s)
    return Markup(s)

def loadhtml_filter(s):
    from datafly.pages import load_html
    return """<article data-id="%s" class="datafly-pages">
               %s
               </article>""" % (s, load_html(s))

def getkey(d, key):
    try:
        return reduce(getitem, key.split("."), d)
    except TypeError:
        return ""

FILTERS = {
    'loadhtml': loadhtml_filter,
    'urlencode': urlencode_filter,
    'getkey': getkey
}

TEMPLATE_SETTINGS = {
    'filters': FILTERS
}

template = functools.partial(template,
                             template_adapter=Jinja2Template,
                             template_settings=TEMPLATE_SETTINGS)

def get_cookie(name):
    return request.get_cookie(name, secret=Config.SECRET)

def set_cookie(name, value, **options):
    return response.set_cookie(name, value, secret=Config.SECRET, path='/', **options)

def delete_cookie(name):
    return response.delete_cookie(name, secret=Config.SECRET, path='/')

# taken from Bottle 0.12 dev
class FileUpload(object):

    def __init__(self, fileobj, name, filename, headers=None):
        ''' Wrapper for file uploads. '''
        #: Open file(-like) object (BytesIO buffer or temporary file)
        self.file = fileobj
        #: Name of the upload form field
        self.name = name
        #: Raw filename as sent by the client (may contain unsafe characters)
        self.raw_filename = filename
        #: A :class:`HeaderDict` with additional headers (e.g. content-type)
        self.headers = HeaderDict(headers) if headers else HeaderDict()

    content_type = HeaderProperty('Content-Type')
    content_length = HeaderProperty('Content-Length', reader=int, default=-1)

    @cached_property
    def filename(self):
        ''' Name of the file on the client file system, but normalized to ensure
            file system compatibility (lowercase, no whitespace, no path
            separators, no unsafe characters, ASCII only). An empty filename
            is returned as 'empty'.
        '''
        from unicodedata import normalize #TODO: Module level import?
        fname = self.raw_filename
        if isinstance(fname, unicode):
            fname = normalize('NFKD', fname).encode('ASCII', 'ignore')
        fname = fname.decode('ASCII', 'ignore')
        fname = os.path.basename(fname.replace('\\', os.path.sep))
        fname = re.sub(r'[^a-zA-Z0-9-_.\s]', '', fname).strip().lower()
        fname = re.sub(r'[-\s]+', '-', fname.strip('.').strip())
        return fname or 'empty'

    def _copy_file(self, fp, chunk_size=2**16):
        read, write, offset = self.file.read, fp.write, self.file.tell()
        while 1:
            buf = read(chunk_size)
            if not buf: break
            write(buf)
        self.file.seek(offset)

    def save(self, destination, overwrite=False, chunk_size=2**16):
        ''' Save file to disk or copy its content to an open file(-like) object.
            If *destination* is a directory, :attr:`filename` is added to the
            path. Existing files are not overwritten by default (IOError).

            :param destination: File path, directory or file(-like) object.
            :param overwrite: If True, replace existing files. (default: False)
            :param chunk_size: Bytes to read at a time. (default: 64kb)
        '''
        if isinstance(destination, basestring): # Except file-likes here
            if os.path.isdir(destination):
                destination = os.path.join(destination, self.filename)
            if not overwrite and os.path.exists(destination):
                raise IOError('File exists.')
            with open(destination, 'wb') as fp:
                self._copy_file(fp, chunk_size)
        else:
            self._copy_file(destination, chunk_size)