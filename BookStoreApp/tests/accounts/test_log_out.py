import pytest


class TestLogOutUnitTest:

    @pytest.mark.django_db
    def test_should_log_out_successfully(self, client, user):

        client.login(username="username", password="password")

        client.logout()

        response = client.get('/accounts/profile/')

        assert response.status_code == 302
        assert response.url == "/accounts/login/?next=/accounts/profile/"

