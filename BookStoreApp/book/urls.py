from django.urls import path
from .views import (
    HomeView,
    BookDetailsView,
    AddFavoriteBook,
    main_search,
    # remove_favorite_book,
    BookListByTag, FavoriteBookDeleteView,
FavoriteBookListView
)

app_name = 'book'

urlpatterns = [
    path('', HomeView.as_view(), name='home_page'),
    path('tag/<int:tag_id>/', BookListByTag.as_view(), name='book_list_by_tag'),
    path('book_detail/<slug:slug>/', BookDetailsView.as_view(), name='book_detail'),
    path('add_favorite_book/<int:id>/', AddFavoriteBook.as_view(), name='add_favorite_book'),
    path('favorites_book_list/', FavoriteBookListView.as_view(), name='favorites_book'),
    path('remove_favorite_book/<int:pk>', FavoriteBookDeleteView.as_view(), name='remove_favorite_book'),
    path('search/', main_search, name='search'),
]
