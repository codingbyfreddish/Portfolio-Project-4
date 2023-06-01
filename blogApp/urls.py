from . import views
from django.urls import path
from .feeds import LatestPostFeed


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('feed/rss', LatestPostFeed(), name='post_feed'),
]