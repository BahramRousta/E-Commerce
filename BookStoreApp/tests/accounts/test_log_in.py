import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestLogInUnitTest:

    def test_log_in_page(self, client):
        sign_in_url = reverse("login")
        response = client.get(sign_in_url)

        assert response.status_code == 200
        assert response.context["request"].path == "/accounts/login/"
        assert response.templates[0].name == "registration/login.html"

    def test_should_log_in_successful_with_valid_username_and_password(self, user, client):
        payload = {
            "next": "",
            "username": "username",
            "password": "password"
        }

        sign_in_url = reverse("login")
        response = client.post(sign_in_url, payload)

        assert response.status_code == 302
        assert response.url == '/accounts/profile/'

    def test_should_log_in_failed_with_invalid_username(self, client):
        payload = {
            "username": "invalid",
            "password": "password"
        }

        sign_in_url = reverse("login")
        response = client.post(sign_in_url, payload, follow=True)

        assert response.redirect_chain == [('/accounts/login/', 302)]
        assert response.templates[0].name == "registration/login.html"

    def test_should_log_in_failed_with_invalid_password(self, user, client):
        payload = {
            "username": "test",
            "password": "invalid"
        }

        sign_in_url = reverse("login")
        response = client.post(sign_in_url, payload, follow=True)

        assert response.redirect_chain == [('/accounts/login/', 302)]
        assert response.templates[0].name == "registration/login.html"
