from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment
from .views import PostDetail, PostLike


class CommentModelTest(TestCase):
    @classmethod
    # Sets up user, a test post, and test comment
    def setUpTestData(cls):
        user = User.objects.create(username='testuser')
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=user,
            content='This is a test post content',
            excerpt='This is a test post excerpt',
            status=1,
        )
        Comment.objects.create(
            post=post,
            name='John Doe',
            email='johndoe@mail.com',
            body='This is a test comment body',
            approved=True,
        )

    # Tests the get method of the PostDetail view
    def test_post_detail_view_get(self):
        user = User.objects.create(username='testuser2')
        client = Client()
        client.force_login(user)
        response = client.get(reverse('post_detail', args=['test-post']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html')
        self.assertEqual(response.context['post'].title, 'Test Post')
        self.assertEqual(len(response.context['comments']), 1)

    # Tests the post method of the PostDetail view
    def test_post_detail_view_post(self):
        user = User.objects.create(username='testuser2')
        client = Client()
        client.force_login(user)
        get_response = client.get(reverse('post_detail', args=['test-post']))
        csrf_token = get_response.cookies['csrftoken'].value
        response = client.post(
            reverse('post_detail', args=['test-post']),
            {
                'body': 'This is a test comment',
                'csrfmiddlewaretoken': csrf_token,
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html')
        self.assertEqual(response.context['commented'], True)


class PostLikeViewTest(TestCase):
    @classmethod
    # Sets up user, a test post, and test comment
    def setUpTestData(cls):
        user = User.objects.create(username='testuser')
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=user,
            content='This is a test post content',
            excerpt='This is a test post excerpt',
            status=1,
        )

    # Tests the post method of the PostLike view
    def test_post_like_view(self):
        factory = RequestFactory()
        request = factory.post(reverse('post_like', args=['test-post']))
        request.user = User.objects.create(username='testuser2')
        response = PostLike.as_view()(request, slug='test-post')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('post_detail', args=['test-post']))
