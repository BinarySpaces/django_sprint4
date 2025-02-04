from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        self.object = self.get_object()
        return self.object.author == self.request.user
