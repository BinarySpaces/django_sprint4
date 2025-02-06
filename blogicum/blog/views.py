from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.urls import reverse, reverse_lazy


from . forms import CommentForm, PostForm, UserProfileForm
from . mixins import OnlyAuthorMixin
from . models import Category, Comment, Post
from . utils import get_user_posts, get_posts_queryset


User = get_user_model()


class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/index.html'

    def get_queryset(self):
        return get_posts_queryset(Post.objects)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={
                'username': self.request.user.username,
            }
        )


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def handle_no_permission(self):
        if not self.test_func():
            return redirect(reverse(
                'blog:post_detail', kwargs={
                    'post_id': self.kwargs.get('post_id')
                }
            ))

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={
                'post_id': self.get_object().pk,
            }
        )


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.get_object())
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        if (post.author == self.request.user or (post.is_published
           and post.category.is_published)):
            return post
        raise Http404('Страница не найдена')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.get_object().comments.order_by('created_at')
        )
        return context


class ProfileView(ListView):
    model = Post
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get_queryset(self):
        profile = get_object_or_404(User, username=self.kwargs.get('username'))
        if profile == self.request.user:
            return get_user_posts(profile.posts)
        else:
            return get_posts_queryset(profile.posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs.get('username')
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'blog/user.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.get_object().username}
        )


class CategoryPostView(ListView):
    model = Post
    template_name = 'blog/category.html'
    paginate_by = 10

    def get_category(self):
        return get_object_or_404(
            Category,
            slug=self.kwargs.get('category_slug'),
            is_published=True
        )

    def get_queryset(self):
        return get_posts_queryset(self.get_category().posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post = get_object_or_404(
            Post,
            pk=self.kwargs.get('post_id')
        )
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={
            'post_id': self.kwargs.get('post_id')
        })


class CommentUpdateView(OnlyAuthorMixin, UpdateView):
    form_class = CommentForm
    success_url = reverse_lazy('blog:index')
    template_name = 'blog/comment.html'

    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs.get('comment_id'))


class CommentDeleteView(OnlyAuthorMixin, DeleteView):
    template_name = 'blog/comment.html'

    def get_object(self):
        return get_object_or_404(Comment, pk=self.kwargs.get('comment_id'))

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={
                'post_id': self.get_object().post.pk,
            }
        )
