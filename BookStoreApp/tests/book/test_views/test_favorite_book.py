import pytest
from django.urls import reverse

from book.models import FavoriteBook


class TestFavoriteBook:

    def setup_method(self):
        self.base_url = "book:favorites_book"

    @pytest.mark.django_db
    def test_favorite_book_list_page(self, client, user):
        client.force_login(user)
        self.favorite_book_url = reverse(self.base_url)
        response = client.get(self.favorite_book_url)

        assert response.status_code == 200
        assert response.templates[0].name == "book/favorites_book.html"
        assert response.context["request"].path == "/favorites_book/"

    @pytest.mark.django_db
    def test_get_favorite_book_list(self, client, favorite_book, user):

        client.force_login(user)
        self.favorite_book_url = reverse(self.base_url)
        response = client.get(self.favorite_book_url)

        assert response.status_code == 200
        assert len(response.context["favorites_book"]) == 1

    @pytest.mark.django_db
    def test_add_new_favorite_book(self, client, user, book):

        client.force_login(user)
        url = reverse("book:add_favorite_book", kwargs={'id': book.id})
        response = client.post(url)

        assert FavoriteBook.objects.count() == 1
        assert response.status_code == 302
        assert response.url == "/books_list/"
