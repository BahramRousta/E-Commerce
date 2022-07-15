from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Book, Author, Category
from taggit.models import Tag
from .utils import my_grouper


def book_list(request, tag_id=None):
    new_publish_book = Book.objects.filter(new_publish=True)
    authors = Author.objects.all()
    tag = None
    if tag_id:
        tag = get_object_or_404(Tag, id=tag_id)

    most_sales_book = Book.objects.get_best_seller()
    return render(request, 'book/index.html', {'most_sales_book': my_grouper(4, most_sales_book),
                                               'new_publish_book': new_publish_book,
                                               'authors': my_grouper(4, authors),
                                               'tag': tag})


class BookListByTag(ListView):
    template_name = 'book/book_list_by_tag.html'
    paginate_by = 4
    context_object_name = 'books'

    def get_queryset(self):
        tag_id = self.kwargs['tag_id']
        books = Book.objects.filter(available=True)
        tag = None
        if tag_id:
            tag = get_object_or_404(Tag, id=tag_id)
            books = books.filter(tags__in=[tag])
        return books

# def book_list_by_tag(request, tag_id=None):
#     books = Book.objects.filter(available=True)
#
#     tag = None
#     if tag_id:
#         tag = get_object_or_404(Tag, id=tag_id)
#         books = books.filter(tags__in=[tag])
#
#     paginator = Paginator(books, 8)
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)
#
#     return render(request, 'book/book_list_by_tag.html', {'tag': tag,
#                                                           'books': books,
#                                                           'page': page,
#                                                           'posts': posts})


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug, available=True)
    author = Author.objects.filter(book__author__book=book)
    author_bio = author.first().description
    author_books = Book.objects.filter(author=author.first())
    category = book.category
    comments = book.book_comment.all()
    tags = book.tags.all()
    return render(request, 'book/book_detail.html', {'book': book,
                                                     'category': category,
                                                     'author_books': author_books,
                                                     'author_bio': author_bio,
                                                     'comments': comments,
                                                     'tags': tags})


