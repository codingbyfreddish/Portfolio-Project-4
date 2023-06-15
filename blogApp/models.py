from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField


STATUS = (
    (0, "Draft"),  # The post is in draft mode and not yet published.
    (1, "Published")  # The post has been published and is visible to readers.
)


class Post(models.Model):
    """
    Represents a blog post.
    This model stores information about a blog post, including its title, author,
    content, creation date, status, and likes. It also provides methods for
    retrieving the number of likes for a post and getting the absolute URL
    for the post's detail view.
    """
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_like', blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': str(self.slug)})


class Comment(models.Model):
    """
    Represents a comment on a blog post.
    This model stores information about a comment, including the associated blog post,
    commenter's name, email, comment body, creation date, and approval status.
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=250)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Comment {self.body} by {self.name}"
