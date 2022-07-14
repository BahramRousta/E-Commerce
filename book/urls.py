from django.urls import path
from .views import book_list, book_detail, book_category, book_list_by_tag

app_name = 'book'

urlpatterns = [
    path('', book_list, name='book_list'),
    path('tag/<int:tag_id>/', book_list_by_tag, name='book_list_by_tag'),
    path('book_detail/<slug:slug>/', book_detail, name='book_detail'),
    path('book_category/<slug:slug>/', book_category, name='book_category'),
]