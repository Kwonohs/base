from django.test import TestCase, Client
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
# Create your tests here.
from .models import Post, Category

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

        self.user_trump = User.objects.create_user(
            username='trump',
            password='1q2w3e4r!'
        )
        self.user_obama = User.objects.create_user(
            username='obama',
            password='1q2w3e4r!'
        )
        self.category_society = Category.objects.create(
            name='society',
            slug='society'
        )

        self.category_economy = Category.objects.create(
            name='economy',
            slug='economy'
        )

        self.category_politic = Category.objects.create(
            name='politic',
            slug='politic'
        )

        self.post1 =Post.objects.create(
            title='1',
            content='1',
            author = self.user_trump,
            category =self.category_politic
        )

        self.post2 =Post.objects.create(
            title='2',
            content='2',
            author = self.user_trump,
            category =self.category_economy,
        )

        self.post3 =Post.objects.create(
            title='3',
            content='3',
            author = self.user_obama,
        )

    def category_card_test(self, bs):
        categories_card = bs.select_one('div#categories-card')

        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_economy.name} ({self.category_economy.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_economy.name} ({self.category_politic.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_economy.name} ({self.category_society.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)

    def test_navbar(self):
        response = self.client.get('/blog/')

        self.assertEqual(response.status_code, 200)

        bs = BeautifulSoup(response.content, 'lxml')

        self.assertEqual(bs.title.text, 'Blog')

        navbar = bs.nav

        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

    def test_post_list(self):
        
        response = self.client.get('/blog/')
        bs = BeautifulSoup(response.content, 'lxml')
        self.assertEqual(Post.objects.count(), 3)

        main_area = bs.select('div#main-area')[0]
        
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        post1_card = main_area.select_one('div#post-1')
        self.assertIn(self.post1.title, post1_card.text)
        self.assertIn(self.post1.category.name, post1_card.text)

        post2_card = main_area.select_one('div#post-2')
        self.assertIn(self.post2.title, post2_card.text)
        self.assertIn(self.post2.category.name, post2_card.text)

        post3_card = main_area.select_one('div#post-3')
        self.assertIn(self.post3.title, post3_card.text)
        # self.assertIn(self.post3.category, post3_card.text)

        self.assertIn(self.post1.title, main_area.text)
        self.assertIn(self.post2.title, main_area.text)
        self.assertIn(self.post3.title, main_area.text)


        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

        self.category_card_test(bs)

        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        bs = BeautifulSoup(response.content, 'lxml')

        main_area = bs.select('div#main-area')[0]
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        

    def test_post_detail(self):
        self.assertEqual(self.post1.get_absolute_url(), '/blog/1')

        response = self.client.get(self.post1.get_absolute_url())

        self.assertEqual(response.status_code, 200)

        bs = BeautifulSoup(response.content, 'lxml')
        self.category_card_test(bs)

        main_area = bs.select_one('div#main-area')
        post_area = main_area.select_one('div#post-area')
        self.assertIn(self.post1.title, post_area.text)
        self.assertIn(self.post1.content, post_area.text)
        self.assertIn(self.user_trump.username.upper(), main_area.text)
        # self.assertIn(self.user_obama.username.upper(), main_area.text)

