import pytest


@pytest.mark.django_db
class TestBookListByTag:

    def setup_method(self):
        pass

    def test_book_list_by_tag_page(self, client, tag):

        response = client.get(f"/tag/{tag.id}/")

        assert response.status_code == 200
        assert response.templates[0].name == "book/book_list_by_tag.html"
        assert response.context['request'].path == "/tag/1/"