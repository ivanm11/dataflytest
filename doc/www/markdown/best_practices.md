BEST PRACTICES
==============

Development with LESS
---------------------

[LESS documentation](http://lesscss.org/#docs)

For asset pipeline install LESS compiler with [npm](https://npmjs.org/),
Node.js required:

```bash
  $ sudo npm install -g less
```

LiveReload
----------

Install Browser [Extension]( http://feedback.livereload.com/knowledgebase/articles/86242-how-do-i-install-and-use-the-browser-extensions).

Install [Python LiveReload](https://github.com/lepture/python-livereload)
package globally:

```bash
  $ sudo pip install livereload
```

Edit `www/Guardfile` if needed.

Start monitoring changes (autoreload browser tab):

```bash
  $ cd www
  $ livereload
```