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

Use in your views:

```python
  from datafly.models.page import Page
  ...
  page = Page.get_latest(page_id)
```

And you still can use PyMongo if you don't need ODM features:

```python
  from config import db

  db.pages.find({'id': id})
```

Document in "pages" collection:

```javascript
{
    "_id" : ObjectId("527062be9fb4e4556cbcaf8a"),
    // id - string, path to page without first slash
    "id" : "home"
    // current version (current content) or outdated
    "current" : true,
    // timestamp - changes are saved
    "published" : ISODate("2013-10-30T01:37:02.601Z"),
    "meta" : {
        "title" : "Home​",
        "description" : "for SEO",
        // timestamp - first version (when this page was created)
        "created" : ISODate("2013-08-16T22:13:07.000Z")
    },    
    // html, id -> value
    "content" : "<h2>HTML</h2>",
    "person1" : "Person 1",
    "person2" : "Person 2",
    "person3" : "Person 3"            
    // images, id -> value
    "img" : {
        "person1" : "http://placehold.it/200x200",
        "person2" : "http://placehold.it/200x200",
        "person3" : "http://placehold.it/200x200",        
    },    
}
```