from django.test import TestCase, Client
from bs4 import BeautifulSoup
# Create your tests here.
from .models import Post

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        response = self.client.get('/blog/')

        self.assertEqual(response.status_code, 200)

        bs = BeautifulSoup(response.content, 'lxml')

        self.assertEqual(bs.title.text, 'Blog')

        navbar = bs.nav

        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        post1 =Post.objects.create(
            title='1',
            content='1'
        )

        post2 =Post.objects.create(
            title='2',
            content='2'
        )

        post3 =Post.objects.create(
            title='3',
            content='3'
        )
        self.assertEqual(Post.objects.count(), 3)

        main_area = bs.select('div#main-area')[0]
        self.assertIn(post1.title, main_area.text)
        self.assertIn(post2.title, main_area.text)
        self.assertIn(post3.title, main_area.text)

        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)



    def test_post_detail(self):
        post_001 = Post.objects.create(
            title="첫 번째 포스트",
            content = "Hello world."
        )

        self.assertEqual(post_001.get_absolute_url(), '/blog/1')

        response = self.client.get(post_001.get_absolute_url())

        self.assertEqual(response.status_code, 200)

        bs = BeautifulSoup(response.content, 'lxml')

        navbar = bs.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        self.assertIn(post_001.title, bs.title.text)

        main_area = bs.select_one('div#main-area')
        post_area = main_area.select_one('div#post-area')
        self.assertIn(post_001.title, post_area.text)
        self.assertIn(post_001.content, post_area.text)