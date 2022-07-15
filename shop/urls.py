from django.urls import path
from .views import BooksList
app_name = 'shop'

urlpatterns = [
    path('books_list/', BooksList.as_view(), name='books_list')
]