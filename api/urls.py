from django.urls import path
from .views import books_list, authors_list

app_name = 'api'

urlpatterns = [
    path('books_list/', books_list, name='books_list'),
    path('authors_list/', authors_list, name='authors_list'),
    # path('categories_list/', categories_list, name='categories_list'),
    # path('book_list_create/', BookListCreateApiView.as_view(), name='book_list_create'),
    # path('book_list/', BookAPIView.as_view(), name='book_list'),
    # path('book_detail/<int:pk>/', DetailBookView.as_view(), name='book_detail'),
]