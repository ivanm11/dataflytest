MODELS
======

Just subclass `Document` from `datafly.odm` to create a model.

Example - `Page` model from `datafly/models`.

```python
  from datafly.odm import Document

  class Page(Document):
    # define MongoDB collection      
    __collection__ = 'pages'
    # add hooks
    def pre_save(self): 
      self['published'] = datetime.utcnow()
```

And you still can use PyMongo if you don't need ODM features:

```python
  from config import db

  db.pages.find({'id': id})
```