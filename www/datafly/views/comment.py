import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pytz import utc
from bottle import Bottle, request, response, abort
from jinja2.filters import do_truncate
from feedgen.feed import FeedGenerator

from datafly.core import g, template
from datafly.models.comment import Comment

from config import Config, db

# PUBLIC

public_app = Bottle()


@public_app.get('/comments')
@public_app.get('/comments/<slug>')
@public_app.get('/comments/page/<page:int>')
def show_comments(page=1, slug=None):
    c = template_context = dict(
        addthis_id = public_app.config.get('addthis_id'),
        fb_id = public_app.config.get('fb_id')
    )
    page = int(page)

    query = {
        'id': { '$regex': 'comment' },
        'current': True,
        'meta.hide': { '$ne': True }
    }

    c['latest_posts'] = db.comments.find(query).sort('meta.created', -1)[0:5]

    c['query'] = search = request.query.get('q', '')
    c['author'] = author = request.query.get('author', None)

    if author:
        query['meta.author'] = author
        comments = db.comments.find(query).sort('meta.created', -1)
    elif len(search):
        # posts from search
        regex = re.compile(search, re.IGNORECASE)
        query['content'] = { '$regex': regex }
        comments = db.comments.find(query).sort('meta.created', -1)
    elif slug:
        # single post
        c['single_comment'] = True
        c['slug'] = slug        
        comment = Comment.get_latest('comments/' + slug)
        hidden = comment['meta'].get('hide', False)
        if hidden == True:
            return abort(404, "Page not found")
        c['comments'] = [comment]
        c['page'] = comment
    else:
        # list
        comments = db.comments.find(query).sort('meta.created', -1)

    if slug is None:
        # pagination
        c['current_page'] = page
        per_page = 100
        skip = (page-1) * per_page
        c['count'] = count = comments.count()
        c['comments'] = comments[skip:skip+per_page]
        c['pages'] = count // 5 + 1 if (count % 5 == 0) else count // 5 + 2

    c['home'] = Comment.get_latest('home')
    print c
    return template('comment.html', **template_context)


@public_app.post('/comments/page/create')
def save_comment():
    text = request.POST.get('text', None)
    print text
    comment = Comment({'text': text, 'id': 'comment/new', 'meta': {'title': '', 'description': ''}})
    comment.save()
    print comment
    return template('simple_comment.html', {'comment': comment})


@public_app.get('/comments/delete/<id>')
def delete_comment(id):
    comment = Comment.get_by_id(id)
    if isinstance(comment, Comment):
        comment.delete()


@public_app.post('/comments/edit/<id>')
def edit_comment(id):
    comment = Comment.get_by_id(id)
    if isinstance(comment, Comment):
        text = request.POST.get('text', None)
        comment['text'] = text
        # comment = Comment({'text': text, 'id': 'comment/new', 'meta': {'title': '', 'description': ''}})
        comment.save()
        # print comment
        return comment['text']
    return 'fail'
# @public_app.get('/blog/rss.xml')
# def rss():
#     config = public_app.config['feed']
#     fg = FeedGenerator()
#     fg.id('%s/blog' % Config.BASE_URL)
#     fg.title(config['title'])
#     fg.author( {'name': config['author'],'email': config['email']} )
#     fg.description(config['desc'])
#     fg.link( href=Config.BASE_URL, rel='alternate' )
#     query = {
#         'id': { '$regex': 'blog' },
#         'current': True,
#         'meta.hide': { '$ne': True }
#     }
#     posts = db.pages.find(query).sort('meta.created', -1)[:20]
#     for post in posts:
#         fe = fg.add_entry()
#         fe.title(post['meta']['title'])
#         if 'author' in post['meta']:
#             fe.author( {'name': post['meta']['author'],'email': config['email']} )
#         else:
#             fe.author( {'name': config['author'],'email': config['email']} )
#         fe.description(do_truncate(post['content'], 300))
#         fe.link(href="%s/%s" % (Config.BASE_URL, post['id']), rel='alternate')
#         fe.pubdate(utc.localize(post['meta']['created']))
#         fe.content(post['content'])
#     response.headers['Content-Type'] = 'application/rss+xml'
#     return fg.rss_str(pretty=True)
#
# # ADMIN
#
# admin_app = Bottle()
#
# @admin_app.get('/admin/blog')
# def blog():
#     posts = (
#         db.pages
#           .find({ 'id': { '$regex': 'blog' }, 'current': True })
#           .sort('meta.created', -1)
#     )
#     return template('admin/blog.html', posts=posts)
#
# @admin_app.get('/admin/blog/:page')
# def edit_blog_post(page):
#     return template('admin/blog-post.html',
#                     editor = True,
#                     page = Page.get_latest(g.page_id))
