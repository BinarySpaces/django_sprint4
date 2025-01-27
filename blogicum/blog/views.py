from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone


from . forms import CongratulationForm, PostForm, ProfileUpdateForm
from . models import Category, Congratulation, Post
from .utils import get_user_posts, posts_queryset


User = get_user_model()


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/index.html'

    def get_queryset(self):
        return posts_queryset(Post.objects)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.pub_date > timezone.now():
            post.is_published = False
        else:
            post.is_published = True
        form.instance.author = self.request.user
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={
                'username': self.object.author.username,
            }
        )


class OnlyAuthorMixin(UserPassesTestMixin):
    """Класс, предназначенный для проверки авторства записи."""

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class PostUpdateView(OnlyAuthorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if post.pub_date > timezone.now():
            post.is_published = False
        else:
            post.is_published = True
        post.save()
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={
                'post_id': self.object.pk,
            }
        )


class PostDeleteView(OnlyAuthorMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:posts_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.get_object())
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CongratulationForm()
        context['comments'] = (
            self.object.congratulations.select_related('author')
        )
        return context


class CategoryPostView(ListView):
    model = Post
    template_name = 'blog/category.html'
    ordering = '-id'
    paginate_by = 10

    def get_category(self, **kwargs):
        return get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )

    def get_queryset(self):
        return get_user_posts(self.get_category().posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context


class CongratulationCreateView(LoginRequiredMixin, CreateView):
    model = Congratulation
    form_class = CongratulationForm

    def get_object(self, queryset=None):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def form_valid(self, form):
        form.instance.post = self.get_object()
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={
            'post_id': self.get_object().pk
        })


class CongratulationUpdateView(UserPassesTestMixin, UpdateView):
    model = Congratulation
    form_class = CongratulationForm
    template_name = 'blog/comment.html'

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_object(self, queryset=None):
        return get_object_or_404(
            Congratulation, pk=self.kwargs['comment_id'],
            post_id=self.kwargs['post_id']
        )

    def test_func(self):
        congratulation = self.get_object()
        return self.request.user == congratulation.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        context['comment'] = self.get_object()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.get_post()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={
                'post_id': self.object.post.pk,
            }
        )


class CongratulationDeleteView(UserPassesTestMixin, DeleteView):
    model = Congratulation
    template_name = 'blog/comment.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Congratulation, pk=self.kwargs['comment_id'])

    def test_func(self):
        congratulation = self.get_object()
        return self.request.user == congratulation.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.object
        return context

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={
                'post_id': self.object.post.pk,
            }
        )


class ProfileView(ListView):
    model = User
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get_queryset(self):
        profile = get_object_or_404(User, username=self.kwargs.get('username'))
        return get_user_posts(profile.posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'profile' not in context:
            context['profile'] = get_object_or_404(
                User, username=self.kwargs.get('username')
            )
        return context


class ProfilUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'profile/user.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs['profile_id'])

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.object.username}
        )
