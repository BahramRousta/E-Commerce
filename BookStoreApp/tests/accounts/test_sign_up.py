import pytest
from django.contrib.auth.models import User
from django.urls import reverse


class TestSignUpUnitTest:

    def test_sign_up_page(self, client):
        sign_up_url = reverse("signup")
        response = client.get(sign_up_url)

        assert response.status_code == 200
        assert response.context["request"].path == "/accounts/signup/"
        assert response.templates[0].name == "registration/signup.html"

    @pytest.mark.django_db
    def test_should_sign_up_successfully_by_new_username_and_email(self, client):
        payload = {
            "username": "user",
            "email": "me@me.com",
            "password": "1",
            "password2": "1"
        }

        sign_up_url = reverse("signup")
        response = client.post(sign_up_url, payload, follow=True)

        assert response.status_code == 200
        assert User.objects.count() == 1
        assert response.redirect_chain == [('/accounts/profile/', 302)]
        assert response.templates[0].name == "registration/profile.html"

    def test_should_sign_up_fail_with_empty_username(self, client):
        payload = {
            "username": "",
            "email": "me@me.com",
            "password": "1",
            "password2": "1"
        }

        sign_up_url = reverse("signup")
        response = client.post(sign_up_url, payload)

        assert response.status_code == 302

    def test_should_sign_up_fail_with_different_password(self, client):

        payload = {
            "username": "user",
            "email": "me@me.com",
            "password": "1",
            "password2": "2"
        }

        sign_up_url = reverse("signup")
        response = client.post(sign_up_url, payload)

        assert response.status_code == 302

    def test_should_sign_up_fail_with_duplicated_email(self, client, user):

        payload = {
            "username": "user",
            "email": user.email,
            "password": "1",
            "password2": "1"
        }

        sign_up_url = reverse("signup")
        response = client.post(sign_up_url, payload)

        assert response.status_code == 302

    def test_should_sign_up_fail_with_duplicated_username(self, client, user):
        payload = {
            "username": user.username,
            "email": user.email,
            "password": "1",
            "password2": "1"
        }

        sign_up_url = reverse("signup")
        response = client.post(sign_up_url, payload)

        assert response.status_code == 302
