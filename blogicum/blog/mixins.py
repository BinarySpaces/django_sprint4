from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from .models import Comment


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        self.object = self.get_object()
        return self.object.author == self.request.user


class CommentMixin(LoginRequiredMixin):
    model = Comment
    template_name = 'blog/comment.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != self.request.user:
            raise PermissionDenied(
                'У вас недостаточно прав для удаления комментария.'
            )
        return super().dispatch(request, *args, **kwargs)
