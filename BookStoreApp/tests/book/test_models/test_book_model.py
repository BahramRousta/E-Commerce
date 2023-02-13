import pytest
from django.db import IntegrityError
from django.utils import timezone
from book.models import Book


class TestBookModel:

    @pytest.mark.django_db
    def test_should_create_new_book_successfully(self, book):
        assert Book.objects.count() == 1
        assert book.title == "book"
        assert book.title == "book"

    @pytest.mark.django_db
    def test_should_fail_create_duplicate_book(self, book, category, publisher, author):
        with pytest.raises(IntegrityError) as model_ex:
            Book.objects.create(title="book",
                                slug="book",
                                category=category,
                                publisher=publisher,
                                published=timezone.now(),
                                price=1000,
                                tags="book_tag")
            book.author.add(author)
            book.save()

        assert 'duplicate key value violates unique constraint' in str(model_ex)
