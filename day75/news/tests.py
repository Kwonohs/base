# from django.test import TestCase, Client
# from bs4 import BeautifulSoup
# # Create your tests here.
# from .models import Post

# class TestView(TestCase):
#     def setUp(self):
#         self.client = Client()

#     def test_post_list(self):
#         response = self.client.get('/blog/')

#         self.assertEqual(response.status_code, 200)

#         bs = BeautifulSoup(response.content, 'lxml')

#         self.assertEqual(bs.title.text, 'Blog')

#         navbar = bs.nav

#         self.assertIn('Blog', navbar.text)
#         self.assertIn('About Me', navbar.text)

#         post1 =Post.objects.create(
#             title='1',
#             content='1'
#         )

#         post2 =Post.objects.create(
#             title='2',
#             content='2'
#         )

#         post3 =Post.objects.create(
#             title='3',
#             content='3'
#         )
#         self.assertEqual(Post.objects.count(), 3)

