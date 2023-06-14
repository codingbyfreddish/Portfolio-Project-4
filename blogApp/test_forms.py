from django.test import TestCase
from .models import Comment
from .forms import CommentForm


class CommentFormTest(TestCase):
    # Tests the form with valid data
    def test_comment_form_valid_data(self):
        form = CommentForm(data={'body': 'This is a test comment'})
        self.assertTrue(form.is_valid())
        comment = form.save(commit=False)
        self.assertEqual(comment.body, 'This is a test comment')
        self.assertIsInstance(comment, Comment)

    # Tests the form with empty data
    def test_comment_form_empty_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['body'], ['This field is required.'])
