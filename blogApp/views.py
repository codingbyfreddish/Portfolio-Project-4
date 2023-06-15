from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from .models import Post
from .forms import CommentForm


class PostList(generic.ListView):
    """
    A view for displaying a list of published blog posts.
    This view retrieves a list of published blog posts from the database and renders
    them using the 'index.html' template. The blog posts are ordered by their creation
    date in descending order. Pagination is applied to display a maximum of 4 posts
    per page.
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 4


class PostDetail(View):
    """
    A view for displaying the details of a blog post and handling comments.
    This view handles both GET and POST requests. For a GET request, it retrieves the
    blog post with the specified slug from the database and renders the 'post_detail.html'
    template with the post details, approved comments, and comment form. It also checks
    if the currently logged-in user has liked the post and includes this information.
    For a POST request, it handles the submission of a new comment. It validates the
    submitted comment form, saves the comment to the database if it is valid, and renders
    the 'post_detail.html' template with the updated comments section and comment form.
    """
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('-created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': False,
                'liked': liked,
                'comment_form': CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('-created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': True,
                'liked': liked,
                'comment_form': CommentForm(),
            },
        )


class PostLike(View):
    """
    A view for handling the like functionality of a blog post.
    This view handles a POST request for toggling the like status of a blog post.
    It receives the slug of the post as a parameter, retrieves the post from the database,
    and checks if the currently logged-in user has already liked the post. If the user has
    already liked the post, their like is removed; otherwise, their like is added.
    After handling the like action, it redirects the user to the 'post_detail' page for the
    respective post.
    """
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
