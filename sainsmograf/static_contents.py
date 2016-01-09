
import datetime
import os
import markdown
from StringIO import StringIO
from functools import partial
from flask import g
from jinja2 import Template

from sainsmograf import app
from sainsmograf.utils import slugify


class PostManager(object):
    def __init__(self, directory=None):
        self.file_contents_dir = 'posts'
        self.directory = self.get_content_dir(directory)
        self.posts = []
        self.tags = []
        self.posts_by_tags = {}

    def get_content_dir(self, directory=None):
        if (not directory):
            contents_dir = app.config.get('STATIC_CONTENTS_DIR', 'contents')

            directory = os.path.join(os.getcwd(), contents_dir, self.file_contents_dir)
            if contents_dir.find('/') == 0:
                directory = os.path.join(contents_dir, self.file_contents_dir)

        return directory

    def load_posts(self):
        self.posts = []

        files = [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]

        for content_file in files:
            if Post.is_post(content_file):
                post = Post.get_post(os.path.join(self.directory, content_file))
                post.process_meta()
                self.posts.append(post)

        # sort post by reverse chronological order
        self.posts = sorted(self.posts, cmp=lambda post1, post2: cmp(post1.date, post2.date), reverse=True)

        # group post by tags
        for post in self.posts:
            for tag in post.tags:
                clean_tag = tag.strip().lower()
                self.tags.append(clean_tag)
                
                tag_posts = self.posts_by_tags.get(clean_tag, [])
                tag_posts.append(post)
                self.posts_by_tags[clean_tag] = tag_posts

        self.tags = list(set(self.tags))
        self.tags.sort()

    def register_views(self, view_func):
        for post in self.posts:
            partial_view_func = partial(view_func, post=post)

            app.add_url_rule(post.url, 'blog-%s-%s' % (post.date.strftime('%Y-%m-%d'), post.slug), partial_view_func)

            print('registered %s to %s' % (post, post.url))


class PageManager(object):
    def __init__(self, directory=None):
        self.file_contents_dir = 'pages'
        self.directory = self.get_content_dir(directory)
        self.pages = []

    def get_content_dir(self, directory=None):
        if (not directory):
            contents_dir = app.config.get('STATIC_CONTENTS_DIR', 'contents')

            directory = os.path.join(os.getcwd(), contents_dir, self.file_contents_dir)
            if contents_dir.find('/') == 0:
                directory = os.path.join(contents_dir, self.file_contents_dir)

        return directory

    def load_pages(self):
        self.pages = []

        files = [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]

        for content_file in files:
            if Page.is_page(content_file):
                page = Page.get_page(os.path.join(self.directory, content_file))
                page.process_meta()
                self.pages.append(page)

    def register_views(self, view_func):
        for page in self.pages:
            partial_view_func = partial(view_func, page=page)

            app.add_url_rule(page.url, 'page-%s' % page.slug, partial_view_func)

            print('registered %s to %s' % (page, page.url))



class Page(object):
    def __init__(self, content_file):
        self.content_file = content_file
        self.title = None
        self.slug = None
        self.url = None
        self.date = None
        self.tags = None
        self.published = False
        self.comments = False
        self.layout = 'post'
        self.format = 'markdown'

    def __str__(self):
        return self.title

    def __repr__(self):
        if self.title:
            return self.title
        else:
            return super(Page, self).__repr__()

    @classmethod
    def is_page(cls, content_file):
        base, ext = os.path.splitext(content_file)
        if ext in ('.md', '.markdown', '.html'):
            return True

        return False

    @classmethod
    def get_page(cls, content_file):
        return Page(content_file)

    def process_meta(self):
        self.parse_header()

    def get_raw_header(self):
        raw_header = None
        dash_counter = 0

        with open(self.content_file) as f:
            for line in f:
                if line.strip() == '---':
                    dash_counter += 1

                if dash_counter == 2:
                    break

                if raw_header is None:
                    raw_header = line.decode('UTF-8')
                else:
                    raw_header += line.decode('UTF-8')

        return raw_header

    def get_raw_content(self):
        raw_content = None
        dash_counter = 0

        with open(self.content_file) as f:
            for line in f:
                if line.strip() == '---':
                    dash_counter += 1
                    continue

                if dash_counter < 2:
                    continue

                if raw_content is None:
                    raw_content = line.decode('UTF-8')
                else:
                    raw_content += line.decode('UTF-8')

        return raw_content

    def parse_header(self):
        base, ext = os.path.splitext(self.content_file)
        if ext in ('.md', '.markdown'):
            self.format = 'markdown'
        elif ext in ('.html',):
            self.format = 'html'

        raw_header = self.get_raw_header()

        import yaml

        page_config = yaml.load(raw_header)

        for key, value in page_config.iteritems():

            if key == 'date':
                value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M')

            if key == 'tags':
                value = value.split(', ')

            setattr(self, key, value)

        if self.slug is None:
            self.slug = slugify(self.title)
            self.unique_slug = '%s-%s' % (self.date.strftime('%Y-%m-%d'), self.slug) if self.date else self.slug


    def get_html_content(self):
        raw_content = self.get_raw_content()

        if self.format == 'html':
            return raw_content

        html = markdown.markdown(raw_content, extensions=['markdown.extensions.codehilite', 'markdown.extensions.footnotes', 'markdown.extensions.tables'])
        return html

    def get_txt_content(self):
        raw_content = self.get_raw_content()

        if self.format == 'html':
            template = Template('{{ content|striptags }}!')
            raw_content = template.render(content=raw_content)
        elif self.format == 'markdown':
            raw_content = markdown.markdown(raw_content, extensions=['markdown.extensions.codehilite', 'markdown.extensions.footnotes', 'markdown.extensions.tables'])
            template = Template('{{ content|striptags }}!')
            raw_content = template.render(content=raw_content)

        return raw_content

    def get_excerpt(self):
        return getattr(self, 'excerpt', self.get_txt_content()[:300]);


class Post(Page):
    def __init__(self, content_file):
        self.content_file = content_file
        self.title = None
        self.slug = None
        self.url = None
        self.date = None
        self.tags = None
        self.published = False
        self.comments = False
        self.layout = 'post'
        self.format = 'markdown'

    @classmethod
    def is_post(cls, content_file):
        base, ext = os.path.splitext(content_file)
        if ext in ('.md', '.markdown', '.html'):
            return True

        return False

    @classmethod
    def get_post(cls, content_file):
        return Post(content_file)

    def parse_header(self):
        super(Post, self).parse_header()

        self.url = '/blog/%s/%s/' % (self.date.strftime('%Y/%m/%d'), self.slug)


def make_views():
    post_manager = PostManager()
    page_manager = PageManager()

    post_manager.load_posts()
    page_manager.load_pages()

    from sainsmograf.views import view_page, view_post

    post_manager.register_views(view_post)
    page_manager.register_views(view_page)

    app.config['post_manager'] = post_manager
    app.config['page_manager'] = page_manager

