from django.shortcuts import render, get_object_or_404
from .models import Book, Author, Category
from taggit.models import Tag
from .utils import my_grouper


def book_list(request, tag_id=None):
    books = Book.objects.filter(available=True)
    new_publish_book = Book.objects.filter(new_publish=True)
    authors = Author.objects.all()
    tag = None
    if tag_id:
        tag = get_object_or_404(Tag, id=tag_id)
    return render(request, 'book/index.html', {'books': my_grouper(4, books),
                                               'new_publish_book': new_publish_book,
                                               'authors': my_grouper(4, authors),
                                               'tag': tag})


def book_list_by_tag(request, tag_id=None):
    books = Book.objects.filter(available=True)
    tag = None
    if tag_id:
        tag = get_object_or_404(Tag, id=tag_id)
        books = books.filter(tags__in=[tag])

    return render(request, 'book/book_list_by_tag.html', {'tag': tag,
                                                          'books': books})


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug, available=True)
    author = Author.objects.filter(book__author__book=book)
    author_bio = author.first().description
    author_books = Book.objects.filter(author=author.first())
    categories = Category.objects.all()
    comments = book.book_comment.all()
    return render(request, 'book/book_detail.html', {'book': book,
                                                     'categories': categories,
                                                     'author_books': author_books,
                                                     'author_bio': author_bio,
                                                     'comments': comments})


def book_category(request, slug):
    return render(request, 'book/book_category.html')
