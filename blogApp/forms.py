from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    """
    A form for creating or updating a comment.
    This form is used to collect user input for creating or updating a comment on a blog post.
    It is based on the `Comment` model and includes the 'body' field.
    """
    class Meta:
        model = Comment
        fields = ('body',)
