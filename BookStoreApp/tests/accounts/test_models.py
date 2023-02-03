from tests.accounts.factories.accounts_factory import UserFactory
from accounts.models import Profile


class TestProfile:

    def test_should_successfully_create_new_profile(self, db):
        user = UserFactory()

        assert Profile.objects.count() == 1
        assert user.profile.user == user
