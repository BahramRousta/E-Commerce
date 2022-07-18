from django.urls import path
from .views import book_list, book_detail, BookListByTag, FavoriteBooks, favorite_book, main_search

app_name = 'book'

urlpatterns = [
    path('', book_list, name='book_list'),
    path('tag/<int:tag_id>/', BookListByTag.as_view(), name='book_list_by_tag'),
    path('book_detail/<slug:slug>/', book_detail, name='book_detail'),
    path('favorite_book/<int:id>/', favorite_book, name='add_favorite_book'),
    path('favorites_book/', FavoriteBooks.as_view(), name='favorites_book'),
    path('search/', main_search, name='search'),
]