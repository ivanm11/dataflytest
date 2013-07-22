# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import functools
from datetime import timedelta
from bottle import (Bottle, request, response, template,
                    static_file, Jinja2Template)

from config import Config
from .jinja2_ext import filters, _globals

try:
    from jinja2_ext import extended_filters, extended_globals
except ImportError:
    extended_filters = extended_globals = {}

# static assets helpers

def get_assets():
    """ Development only. Return list of relative paths for LESS, JS assets"""    
    return dict(
        less = Config.LESS,
        js = Config.JS
    )

assets_app = Bottle()

@assets_app.get('/js/<filename:path>')
@assets_app.get('/less/<filename:path>')
@assets_app.get('/static/<filename:path>')
@assets_app.get('/datafly/<filename:path>')
def static(filename):
    d, filename = os.path.split(request.path)
    return static_file(filename, '.' + d + '/')

# shortcuts to cookie methods

def get_cookie(name):
    return request.get_cookie(name, secret=Config.SECRET)

def set_cookie(name, value, temporary=False, **options):
    if 'max_age' not in options and not temporary:
        options['max_age'] = timedelta(days=30)
    return response.set_cookie(name, value, secret=Config.SECRET, path='/', **options)

def delete_cookie(name):
    return response.delete_cookie(name, secret=Config.SECRET, path='/')

def get_route():
    return request.environ['bottle.route']

# thread-safe global variables for Bottle

class _AppCtxGlobals(object):
    """ Globals for Bottle - thread safe data storage
        Shortcut to request.g
    """

    def __getattr__(self, name):
        return request.g.get(name, None)

    def __setattr__(self, name, value):
        request.g[name] = value

    def _reset(self):
        request.g = {}

    def _inspect(self):
        g = request.g.copy()
        g.pop('template_context')
        return g

g = _AppCtxGlobals()

# Jinja2 configuration

# add project specific filters to default filters
filters.update(extended_filters)
_globals.update(extended_globals)

template_settings = {
    'filters': filters,
    '_globals': _globals
}

template_lookup = {
    './templates',
    './datafly/',
    '.'
}

class Jinja2TemplateSafeDefaults(Jinja2Template):
    def prepare(self, filters=None, tests=None, _globals=None, **kwargs):
        """
            patch for env.globals Jinja2 issue
            https://github.com/defnull/bottle/pull/423
        """
        from jinja2 import Environment, FunctionLoader
        if 'prefix' in kwargs: # TODO: to be removed after a while
            raise RuntimeError('The keyword argument `prefix` has been removed. '
                'Use the full jinja2 environment name line_statement_prefix instead.')
        self.env = Environment(loader=FunctionLoader(self.loader), **kwargs)
        if filters: self.env.filters.update(filters)                
        if tests: self.env.tests.update(tests)
        if _globals: self.env.globals.update(_globals)
        if self.source:
            self.tpl = self.env.from_string(self.source)
        else:
            self.tpl = self.env.get_template(self.filename)

    def render(self, *args, **kwargs):
        for dictarg in args: kwargs.update(dictarg)
        # Bottle self.defaults are not thread-safe
        # were replaced by g.template_context
        _defaults = g.template_context
        _defaults.update(kwargs)
        return self.tpl.render(**_defaults)
    
template = functools.partial(template,
                             template_adapter=Jinja2TemplateSafeDefaults,
                             template_lookup=template_lookup,
                             template_settings=template_settings)

# various Bottle helpers

def print_routes(app):
    """ Inspect all the routes (including mounted sub-apps)
        for the root Bottle application
    """
    def inspect_routes(app):
        for route in app.routes:
            if 'mountpoint' in route.config:
                prefix = route.config['mountpoint']['prefix']
                subapp = route.config['mountpoint']['target']

                for prefixes, route in inspect_routes(subapp):
                    yield [prefix] + prefixes, route
            else:
                yield [], route
    for prefixes, route in inspect_routes(app):
        abs_prefix = '/'.join(part for p in prefixes for part in p.split('/'))
        print abs_prefix, route.name, route.rule, route.method, route.callback

# FileUpload - taken from Bottle 0.12 dev

import re
from bottle import cached_property, HeaderDict, HeaderProperty

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