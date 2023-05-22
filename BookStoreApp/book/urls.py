from django.urls import path
from .views import (
    HomeView,
    BookDetailsView,
    FavoriteBooks,
    main_search,
    remove_favorite_book,
    BookListByTag
)

app_name = 'book'

urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('tag/<int:tag_id>/', BookListByTag.as_view(), name='book_list_by_tag'),
    path('book_detail/<slug:slug>/', BookDetailsView.as_view(), name='book_detail'),
    path('favorite_book/<int:id>/', FavoriteBooks.as_view(), name='add_favorite_book'),
    path('favorites_book/', FavoriteBooks.as_view(), name='favorites_book'),
    path('remove_favorite_book/<int:id>', remove_favorite_book, name='remove_favorite_book'),
    path('search/', main_search, name='search'),
]
