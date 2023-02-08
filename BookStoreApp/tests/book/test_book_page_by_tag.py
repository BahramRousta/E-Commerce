import pytest


class TestBookListByTag:

    def setup_method(self):
        pass

    @pytest.mark.django_db
    def test_book_list_by_tag_page(self, client, book):

        response = client.get(f"/tag/{book.tags.id}/")

        assert response.status_code == 200
        assert response.templates[0].name == "book/book_list_by_tag.html"
        assert response.context['request'].path == "/tag/1/"