import pytest
from django.urls import reverse
from django.utils import timezone

from book.models import Book


class TestBookDetail:

    def setup_method(self):
        self.base_url = "book:book_detail"

    @pytest.mark.django_db
    def test_book_detail_page(self, client, book):

        self.detail_url = reverse(self.base_url, kwargs={"slug": book.slug})
        response = client.get(self.detail_url)

        assert response.status_code == 200
        assert response.context["request"].path == f"/book_detail/{book.slug}/"
        assert response.templates[0].name == "book/book_detail.html"

    @pytest.mark.django_db
    def test_book_detail_page_object(self, client, book):

        self.detail_url = reverse(self.base_url, kwargs={"slug": book.slug})
        response = client.get(self.detail_url)

        assert response.context["book"] == book
        assert response.context["book_categories"] == book.category

