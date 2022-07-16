from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView

from .models import Book, Author, Category, FavoriteBook
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

    author = Author.objects.filter(book=book)

    author_bio = author.first().description

    author_books = Book.objects.filter(author__book=book).exclude(id=book.id)

    book_categories = book.category
    # Get Similar Book
    similar_books = Book.objects.filter(category=book_categories).exclude(id=book.id)
    # Get comments
    comments = book.book_comment.all()
    # Get tags
    tags = book.tags.all()
    return render(request, 'book/book_detail.html', {'book': book,
                                                     'book_categories': book_categories,
                                                     'author_books': author_books,
                                                     'author_bio': author_bio,
                                                     'comments': comments,
                                                     'tags': tags,
                                                     'similar_books': my_grouper(4, similar_books)})


class FavoriteBooks(View):
    template_name = 'book/favorites_book.html'
    context_object_name = 'favorites_book'

    def get(self, request, *args, **kwargs):
        self.username = request.user.username
        self.favorites_book = FavoriteBook.objects.filter(user=self.username)
        return render(request, self.template_name, {'favorites_book': self.favorites_book})

    def post(self, request, id, *args, **kwargs):
        self.book = Book.objects.get(id=id)

        self.favorite = None
        if FavoriteBook.objects.filter(user=request.user.username, book=self.book).exists():
            return redirect('shop:books_list')
        else:
            favorite = FavoriteBook.objects.create(user=request.user.username, book=self.book)
            return redirect('shop:books_list')
