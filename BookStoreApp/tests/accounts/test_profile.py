import pytest
from django.urls import reverse


class TestProfile:

    def setup_method(self):
        self.base_url = reverse("profile")

    @pytest.mark.django_db
    def test_should_authorized_user_see_profile_page(self, user, client):

        client.force_login(user)
        response = client.get(self.base_url)

        assert response.status_code == 200
        assert response.templates[0].name == "registration/profile.html"

    def test_should_un_authorize_user_redirected_to_login_page(self, client):
        response = client.get(self.base_url)

        assert response.status_code == 302
        assert response.url == "/accounts/login/?next=/accounts/profile/"

    def teardown_method(self):
        pass