from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, TemplateView
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .models import Book, Author, Category, FavoriteBook, SearchHistory
from taggit.models import Tag
from .utils import my_grouper
from .signals import CACHE_KEY_PREFIX


class HomeView(TemplateView):
    template_name = 'book/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        new_publish_book = Book.objects.filter(new_publish=True).select_related('category', 'publisher')
        authors = Author.objects.all()

        tag_id = self.kwargs.get('tag_id')
        tag = None
        if tag_id:
            tag = get_object_or_404(Tag, id=tag_id)

        most_sales_book = Book.objects.get_best_seller()

        context['new_publish_book'] = new_publish_book
        context['authors'] = my_grouper(4, authors)
        context['most_sales_book'] = my_grouper(4, most_sales_book)
        context['tags'] = tag

        return context


# @cache_page(180, key_prefix=CACHE_KEY_PREFIX)
# def home_page(request, tag_id=None, *args, **kwargs):
#
#     new_publish_book = Book.objects.filter(new_publish=True)
#     authors = Author.objects.all()
#
#     tag = None
#     if tag_id:
#         tag = get_object_or_404(Tag, id=tag_id)
#
#     most_sales_book = Book.objects.get_best_seller()
#
#     return render(request, 'book/index.html', {'most_sales_book': my_grouper(4, most_sales_book),
#                                                'new_publish_book': new_publish_book,
#                                                'authors': my_grouper(4, authors),
#                                                'tag': tag})



class BookListByTag(ListView):
    template_name = 'book/book_list_by_tag.html'
    paginate_by = 4
    context_object_name = 'books'

    def get_queryset(self):
        tag_id = self.kwargs['tag_id']

        if tag_id:
            tag = get_object_or_404(Tag, id=tag_id)
            books = Book.objects.filter(
                available=True, tags__in=[tag]
            ).prefetch_related(
                'tags'
            ).distinct()

            return books


@cache_page(180, key_prefix=CACHE_KEY_PREFIX)
def book_detail(request, slug):

    book = Book.objects.filter(slug=slug, available=True).select_related('category', 'publisher').first()
    # book = get_object_or_404(Book, slug=slug, available=True).select_related
    author = Author.objects.filter(authors_book=book).prefetch_related('authors_book')
    author_bio = author.first().description

    # Get author other books
    author_books = Book.objects.filter(author=author.first()).exclude(id=book.id)
    # book_categories = book.category

    similar_books = book.category.book_categories.prefetch_related('author').exclude(id=book.id)
    # Get Similar Book
    # similar_books = Book.objects.filter(category=book_categories).exclude(id=book.id)

    # Get comments
    comments = book.book_comment.all()

    # Get tags
    tags = book.tags.all()
    return render(request, 'book/book_detail.html', {'book': book,
                                                     'book_categories': book.category,
                                                     'author_books': author_books,
                                                     'author_bio': author_bio,
                                                     'comments': comments,
                                                     'tags': tags,
                                                     'similar_books': my_grouper(4, similar_books)})


class FavoriteBooks(LoginRequiredMixin, View):
    login_url = 'accounts/login/'
    template_name = 'book/favorites_book.html'
    context_object_name = 'favorites_book'

    def get(self, request, *args, **kwargs):
        self.username = request.user.username
        self.favorites_book = FavoriteBook.objects.filter(user=self.username)
        return render(request, self.template_name, {'favorites_book': self.favorites_book})

    def post(self, request, id, *args, **kwargs):
        self.book = Book.objects.get(id=id)
        self.current_user = request.user
        self.favorite = None

        try:
            self.favorite = FavoriteBook.objects.filter(user=self.current_user.username, book=self.book).exists()
            return redirect('shop:books_list')
        except:
            self.favorite = FavoriteBook.objects.create(user=self.current_user.username, book=self.book)

        return redirect('shop:books_list')


@login_required(login_url='/accounts/login/')
def favorite_book(request, id):
    user = request.user.username
    book = get_object_or_404(Book, id=id)
    favorite = None
    if request.method == "POST":

        if request.user.is_authenticated:

            if FavoriteBook.objects.filter(user=user, book=book).exists():
                return redirect('shop:books_list')
            else:
                FavoriteBook.objects.create(user=user, book=book)
                return redirect('shop:books_list')
        else:
            return HttpResponseRedirect('login/')
    else:
        return redirect('shop:books_list')


@login_required(login_url='/accounts/login/')
def remove_favorite_book(request, id):
    current_book = Book.objects.get(id=id)
    favorite_book = FavoriteBook.objects.filter(user=request.user).all()

    for favorite in favorite_book:
        if favorite.book.id == current_book.id:
            favorite.delete()

    return redirect('book:favorites_book')


def main_search(request):
    query = None
    results = []

    if 'query' in request.GET:
        query = request.GET.get('query')
        # search_vector = SearchVector('title', weight='A') + \
        #                 SearchVector('description', weight='B')
        # search_query = SearchQuery(query)
        #
        # results = Book.objects.annotate(
        #     search=search_vector,
        #     rank=SearchRank(search_vector, search_query)
        # ).filter(rank__gte=0.3).order_by('-rank')
        new_search = SearchHistory.objects.create(user_id=request.user.id,
                                                  query=query)
        results = Book.objects.annotate(
            search=SearchVector('title', 'author__name'),
        ).filter(search=query)

    return render(request, 'book/search.html', {'query': query,
                                                'results': results})
