from django.test import TestCase, Client
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag, Comment
from bs4 import BeautifulSoup

# Create your tests here.

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_trump = User.objects.create_user(
            username='trump',
            password='1q2w3e4r!',
        )

    def test_landing(self):
        self.post1 = Post.objects.create(
            title='가나다라',
            content='마바사',
            author=self.user_trump,
        )

        self.post2 = Post.objects.create(
            title='아자차카',
            content='타파하',
            author=self.user_trump,
        )

        self.post3 = Post.objects.create(
            title='가갸거겨고교',
            content='구규그기',
            author=self.user_trump,
        )

        self.post4 = Post.objects.create(
            title='나나너노뇨',
            content='누뉴느니',
            author=self.user_trump,
        )

    def test_landing(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        bs = BeautifulSoup(response.content, 'lxml')

        body = bs.body
        self.assertNotIn(self.post1.title, body.text)
        self.assertIn(self.post2.title, body.text)
        self.assertIn(self.post3.title, body.text)
        self.assertIn(self.post4.title, body.text)
