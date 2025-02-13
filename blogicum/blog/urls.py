from django.urls import path

from .import views

app_name = 'blog'

urlpatterns = [
    # С пустыми строками проще ориентироваться.
    path('',
         views.PostListView.as_view(),
         name='index'),

    path('posts/create/',
         views.PostCreateView.as_view(),
         name='create_post'),

    path('posts/<int:post_id>/',
         views.PostDetailView.as_view(),
         name='post_detail'),

    path('category/<slug:category_slug>/',
         views.CategoryPostView.as_view(),
         name='category_posts'),

    path('posts/<int:post_id>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post'),

    path('posts/<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post'),

    path('posts/<int:post_id>/comment/',
         views.CommentCreateView.as_view(),
         name='add_comment'),

    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.CommentUpdateView.as_view(),
         name='edit_comment'),

    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.CommentDeleteView.as_view(),
         name='delete_comment'),

    path('profile/<str:username>/',
         views.ProfileView.as_view(),
         name='profile'),

    path('edit/profile/',
         views.ProfileUpdateView.as_view(),
         name='edit_profile'),
]
