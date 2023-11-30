from django.contrib.auth.mixins import UserPassesTestMixin


class IsOwner(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            task = self.get_object()
            return task.owner == self.request.user
        return False
