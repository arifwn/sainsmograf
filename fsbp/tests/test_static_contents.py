
import datetime
import unittest

from fsbp.static_contents import PostManager, Post, PageManager, Page

class TestPostMarkdown(unittest.TestCase):
    def setUp(self):
        self.post = Post('contents/posts/2013-07-15-encryption-primer.markdown')

    def test_meta(self):
        self.post.process_meta()
        self.assertEqual(self.post.title, 'Cryptography Primer')
        self.assertEqual(self.post.slug, 'cryptography-primer')
        self.assertEqual(self.post.url, '/blog/2013/07/15/cryptography-primer/')
        self.assertEqual(self.post.date, datetime.datetime(2013, 7, 15, 20, 37))
        self.assertEqual(self.post.tags, ['security'])
        self.assertEqual(self.post.published, True)
        self.assertEqual(self.post.comments, True)
        self.assertEqual(self.post.layout, 'post')
        self.assertEqual(self.post.format, 'markdown')

    def test_content(self):
        raw_content = self.post.get_raw_content()
        html_content = self.post.get_html_content()


class TestPostManager(unittest.TestCase):
    def setUp(self):
        self.manager = PostManager()

    def test_load_posts(self):
        self.manager.load_posts()

        # print(self.manager.tags)
        # print(self.manager.posts_by_tags)


class TestPageMarkdown(unittest.TestCase):
    def setUp(self):
        self.page = Page('contents/pages/about.markdown')

    def test_meta(self):
        self.page.process_meta()
        self.assertEqual(self.page.title, 'About Me')
        self.assertEqual(self.page.url, '/about/')
        self.assertEqual(self.page.comments, False)
        self.assertEqual(self.page.layout, 'page')
        self.assertEqual(self.page.format, 'markdown')

    def test_content(self):
        raw_content = self.page.get_raw_content()
        html_content = self.page.get_html_content()


class TestPageManager(unittest.TestCase):
    def setUp(self):
        self.manager = PageManager()

    def test_load_posts(self):
        self.manager.load_pages()

        # print(self.manager.pages)
