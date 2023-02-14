import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestCartPage:

    def setup_method(self):
        self.url = reverse("cart")

    def test_cart_page(self, user, client):
        client.force_login(user)

        response = client.get(self.url)

        assert response.status_code == 200
        assert response.context["request"].path == "/cart/"
        assert response.templates[0].name == "cart/cart.html"

    def test_cart_page_must_redirect_to_login_page_for_unauthorized_user(self, client):

        response = client.get(self.url)

        assert response.status_code == 302


