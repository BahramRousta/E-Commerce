import pytest
from django.urls import reverse


class TestBookDetail:

    @pytest.mark.django_db
    def test_book_detail_page(self, client, book):
        base_url = reverse("book:book_detail", kwargs={"slug": book.slug})

        response = client.get(base_url)

        assert response.status_code == 200
        assert response.context["request"].path == f"/book_detail/{book.slug}/"
        assert response.templates[0].name == "book/book_detail.html"




