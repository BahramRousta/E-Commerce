from django.urls import path
from .views import (
    home_page,
    book_detail,
    BookListByTag,
    FavoriteBooks,
    favorite_book,
    main_search,
    remove_favorite_book
)

app_name = 'book'

urlpatterns = [
    path('', home_page, name='home_page'),
    path('tag/<int:tag_id>/', BookListByTag, name='book_list_by_tag'),
    path('book_detail/<slug:slug>/', book_detail, name='book_detail'),
    path('favorite_book/<int:id>/', favorite_book, name='add_favorite_book'),
    path('favorites_book/', FavoriteBooks.as_view(), name='favorites_book'),
    path('remove_favorite_book/<int:id>', remove_favorite_book, name='remove_favorite_book'),
    path('search/', main_search, name='search'),
]
