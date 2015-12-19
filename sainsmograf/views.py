
from datetime import datetime
from flask import Flask, url_for, redirect
from flask import Response, render_template
from flask import g

from sainsmograf import app

@app.route('/')
def index():
    return render_template('index.html', static_navbar=True)


@app.route('/atom.xml')
def atom():
    now = datetime.utcnow()
    xml = render_template('atom.xml', date=now, posts=app.config['post_manager'].posts)
    return Response(xml, mimetype='text/xml')


@app.route('/sitemap.xml')
def sitemap():
    links = []

    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))

    now = datetime.utcnow()
    xml = render_template('sitemap.xml', date=now, links=links)
    return Response(xml, mimetype='text/xml')


@app.route('/favicon.png')
def favicon():
    return redirect('/static/img/favicon.png')

@app.route('/favicon.ico')
def favicon_ico():
    return redirect('/static/img/favicon.png')


@app.route('/CNAME')
def cname():
    return app.config.get('TARGET_SERVER_NAME', 'localhost')


@app.route('/robots.txt')
def robots():
    return '''
User-agent: *
Disallow: 

Sitemap: http://www.sainsmograf.com/sitemap.xml 
    '''


@app.route('/blog/')
def blog_index():
    with app.test_request_context():
        return render_template('blog-index.html', posts=app.config['post_manager'].posts)

@app.route('/tags/')
def tags_index():
    with app.test_request_context():
        return render_template('tags-index.html', tags=app.config['post_manager'].tags)


def view_page(page):
    return render_template('layouts/%s.html' % page.layout, post=page)


def view_post(post):
    return render_template('layouts/%s.html' % post.layout, post=post)


def view_tag(tag, posts):
    return render_template('blog-index.html', title=tag.upper(), posts=posts)


@app.template_filter()
def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.utcnow()
    diff = now - dt
    
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default
