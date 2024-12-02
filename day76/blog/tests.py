from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Post, Category, Tag
from bs4 import BeautifulSoup
# Create your tests here.


class TestView(TestCase):
    def setUp(self):
        # 테스트를 실행하기 전에 Client 객체를 생성하여 요청을 보낼 준비를 합니다.
        self.client = Client()

        self.user_trump = User.objects.create_user(
            username='trump',
            password='1q2w3e4r!',
        )
        self.user_trump.is_staff = True
        self.user_trump.save()
        self.user_obama = User.objects.create_user(
            username='obama',
            password='1q2w3e4r!',
        )

        self.category_society = Category.objects.create(
            name='society',
            slug='society',
        )
        self.category_economy = Category.objects.create(
            name='economy',
            slug='economy',
        )
        self.category_politic = Category.objects.create(
            name='politic',
            slug='politic',
        )

        # tag
        self.tag_python_kor = Tag.objects.create(
            name='파이썬 공부',
            slug='파이썬-공부',
        )
        self.tag_python = Tag.objects.create(
            name='python',
            slug='python',
        )
        self.tag_hello = Tag.objects.create(
            name='hello',
            slug='hello',
        )

        # 새로운 게시글 3개를 데이터베이스에 생성
        self.post1 = Post.objects.create(
            title='가나다라',
            content='마바사',
            author=self.user_trump,
            category=self.category_politic,
        )
        self.post1.tags.add(self.tag_hello)

        self.post2 = Post.objects.create(
            title='아자차카',
            content='타파하',
            author=self.user_trump,
            category=self.category_economy,
        )

        self.post3 = Post.objects.create(
            title='가갸거겨고교',
            content='구규그기',
            author=self.user_obama,
        )
        self.post3.tags.add(self.tag_python_kor)
        self.post3.tags.add(self.tag_python)

    def category_card_test(self, bs):
        categories_card = bs.select_one('div#categories-card')

        self.assertIn('Categories', categories_card.text)
        self.assertIn(f'{self.category_economy.name} ({self.category_economy.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_politic.name} ({self.category_politic.post_set.count()})', categories_card.text)
        self.assertIn(f'{self.category_society.name} ({self.category_society.post_set.count()})', categories_card.text)
        self.assertIn(f'미분류 (1)', categories_card.text)

    def test_navbar(self):
        # 블로그 페이지에 GET 요청을 보내고 응답 상태 코드가 200인지 확인
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        # BeautifulSoup을 사용해 HTML을 파싱하고 title 태그의 내용을 확인
        bs = BeautifulSoup(response.content, 'lxml')
        self.assertEqual(bs.title.text, 'Blog')

        # 네비게이션 바(nav) 내에 'Blog'와 'About Me' 링크가 있는지 확인
        navbar = bs.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

    def test_post_list(self):
        # 데이터베이스에 게시물이 3개가 맞는지 확인
        self.assertEqual(Post.objects.count(), 3)

        # 블로그 페이지에 다시 GET 요청을 보내고 응답 상태 코드가 200인지 확인
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        # BeautifulSoup을 사용해 HTML을 파싱하고 'main-area' div가 있는지 확인
        bs = BeautifulSoup(response.content, 'lxml')

        # category section test
        self.category_card_test(bs)

        # 'main-area' div 안에 각 게시물의 제목이 포함되어 있는지 확인
        main_area = bs.select('div#main-area')[0]

        # '아직 게시물이 없습니다.'라는 텍스트가 포함되지 않았는지 확인
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        post1_card = main_area.select_one('div#post-1')
        self.assertIn(self.post1.title, post1_card.text)
        self.assertIn(self.post1.category.name, post1_card.text)
        self.assertIn(self.tag_hello.name, post1_card.text)
        self.assertNotIn(self.tag_python_kor.name, post1_card.text)
        self.assertNotIn(self.tag_python.name, post1_card.text)

        post2_card = main_area.select_one('div#post-2')
        self.assertIn(self.post2.title, post2_card.text)
        self.assertIn(self.post2.category.name, post2_card.text)
        self.assertNotIn(self.tag_hello.name, post2_card.text)
        self.assertNotIn(self.tag_python_kor.name, post2_card.text)
        self.assertNotIn(self.tag_python.name, post2_card.text)

        post3_card = main_area.select_one('div#post-3')
        self.assertIn(self.post3.title, post3_card.text)
        self.assertIsNone(self.post3.category)
        self.assertNotIn(self.tag_hello.name, post3_card.text)
        self.assertIn(self.tag_python_kor.name, post3_card.text)
        self.assertIn(self.tag_python.name, post3_card.text)
       
        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

        # 게시글이 없을 때
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        # BeautifulSoup을 사용해 HTML을 파싱하고 'main-area' div가 있는지 확인
        bs = BeautifulSoup(response.content, 'lxml')

        # 'main-area' div 안에 각 게시물의 제목이 포함되어 있는지 확인
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
        self.assertIn(self.category_politic.name, post_area.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.post1.content, post_area.text)

    def test_category_page(self):
        response = self.client.get(self.category_politic.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        bs = BeautifulSoup(response.content, 'lxml')
        self.category_card_test(bs)

        self.assertIn(self.category_politic.name, bs.h1.text)

        main_area = bs.select_one('div#main-area')
        self.assertIn(self.category_politic.name, main_area.text)
        self.assertIn(self.post1.title, main_area.text)

    def test_tag_page(self):
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        bs = BeautifulSoup(response.content, 'lxml')
        self.category_card_test(bs)

        self.assertIn(self.tag_hello.name, bs.h1.text)

        main_area = bs.select_one('div#main-area')
        self.assertIn(self.tag_hello.name, main_area.text)
        self.assertIn(self.post1.title, main_area.text)
        self.assertNotIn(self.post2.title, main_area.text)
        self.assertNotIn(self.post3.title, main_area.text)

    def test_create_post(self):
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username='trump', password='1q2w3e4r!')
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)

        self.client.login(username='obama', password='1q2w3e4r!')
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        bs = BeautifulSoup(response.content, 'lxml')


        self.assertEqual('Create Post - Blog', bs.title.text)
        main_area = bs.select_one('div#main-area')
        self.assertIn('Create New Post' , main_area.text)

        self.client.post(
            '/blog/create_post/',
            {
                'title': 'Post Form 만들기',
                'content': 'Post Form 페이지 만들기',
            }
        )
        self.assertEqual(Post.objects.count(), 4)
        last_post = Post.objects.last()
        self.assertEqual(last_post.title, "Post Form 만들기")
        self.assertEqual(last_post.author.username, 'trump')

    def test_update_post(self):
        update_post_url = f'/blog/update_post/{self.post1.pk}'

        response = self.client.request(update_post_url)
        self.assertNotEqual(response.status_code, 200)

        self.assertNotEqual(self.post1.author, self.user_obama)
        self.client.login(
            usename=self.user_obama.username,
            password='1q2w3e4r!',
        )

        response = self.client.request(update_post_url)
        self.assertEqual(response.status_code, 403)

        self.client.login(
            usename=self.user_trump.username,
            password='1q2w3e4r!',
        )

        response = self.client.request(update_post_url)
        self.assertEqual(response.status_code, 200)

        bs = BeautifulSoup(response.content, 'lxml')

        self.assertEqual('Edit Post - Blog', bs.title.text)
        main_area = bs.select_one('div#main-area')
        self.assertIn('Edit Post', main_area.text)

        response = self.client.post(
            update_post_url,
            {
                'title': '세 번째 포스트 수정',
                'content': '4교시다',
                'category': self.category_economy.pk,
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        bs = BeautifulSoup(response.content, 'lxml')
        main_area = bs.select_one('div#main-area')
        self.assertIn('세 번째 포스트 수정', bs.title.text)
        self.assertIn('4교시다.', main_area.text)
        self.assertIn(self.category_economy.name, main_area.text)
        