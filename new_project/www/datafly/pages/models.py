from datetime import datetime
from bottle import cached_property

from datafly.odm import Document

from config import db

class Page(Document):
    __collection__ = 'pages'

    @cached_property
    def versions(self):        
        return db.pages.find(
            { 'id': self['id'] },
            { 'published': 1 }
        ).sort('_id', -1)

    @classmethod
    def get_latest(cls, _id):
        pages = list(
            cls.find({'id': _id})
               .sort('published', -1)
               .limit(1)
        )
        if len(pages):
            return pages.pop()

    def pre_save(self):        
        self['published'] = datetime.utcnow()                
        self.set_as_current()
        self.set_created()

    def set_created(self):
        created = self['meta'].get('created', None)                
        if created:
            if isinstance(created, datetime):
                return
            DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
            self['meta']['created'] = datetime.strptime(self['meta']['created'],
                                                        DATETIME_FORMAT)
        else:
            self['meta']['created'] = datetime.utcnow()

    def set_as_current(self):
        db.pages.update({ 'id': self['id'] },
                    { '$unset': { 'current': True } },
                    multi=True)
        self['current'] = True