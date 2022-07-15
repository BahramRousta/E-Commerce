from django.urls import path
from .views import book_list, book_detail, BookListByTag

app_name = 'book'

urlpatterns = [
    path('', book_list, name='book_list'),
    path('tag/<int:tag_id>/', BookListByTag.as_view(), name='book_list_by_tag'),
    path('book_detail/<slug:slug>/', book_detail, name='book_detail'),
]