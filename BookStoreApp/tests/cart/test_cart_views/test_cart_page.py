import pytest
from django.urls import reverse


class TestCartPage:

    @pytest.mark.django_db
    def test_cart_page(self, user, client):
        client.force_login(user)
        self.url = reverse("cart")

        response = client.get(self.url)

        assert response.status_code == 200
        assert response.context["request"].path == "/cart/"
        assert response.templates[0].name == "cart/cart.html"

    @pytest.mark.django_db
    def test_cart_page_must_redirect_to_login_page_for_unauthorized_user(self, user, client):
        url = reverse("cart")
        response = client.get(url)

        assert response.status_code == 302


