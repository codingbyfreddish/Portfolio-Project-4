from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment


class PostModelTest(TestCase):
    @classmethod
    # Sets up a user and test post
    def setUpTestData(cls):
        user = User.objects.create(username='testuser')
        Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=user,
            content='This is a test post content',
            excerpt='This is a test post excerpt',
            status=1,
        )

    # Tests the number_of_likes method of the Post model
    def test_number_of_likes(self):
        post = Post.objects.get(title='Test Post')
        self.assertEqual(post.number_of_likes(), 0)


class CommentModelTest(TestCase):
    @classmethod
    # Sets up a users, a test post, and test comment
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

    # Tests the __str__ method and compares it to the expected string
    def test_comment_str_representation(self):
        comment = Comment.objects.get(body='This is a test comment body')
        expected_str = f"Comment {comment.body} by {comment.name}"
        self.assertEqual(str(comment), expected_str)

    # Tests that the comments are ordered by -created on
    def test_comment_ordering(self):
        post = Post.objects.get(title='Test Post')
        Comment.objects.create(
            post=post,
            name='Jane Smith',
            email='janesmith@mail.com',
            body='This is also a test comment',
            approved=True,
        )
        comments = Comment.objects.filter(post=post)
        self.assertEqual(comments.count(), 2)
        self.assertEqual(comments[0].name, 'John Doe')
        self.assertEqual(comments[1].name, 'Jane Smith')
