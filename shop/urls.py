from django.urls import path
from .views import BooksList, about_us
app_name = 'shop'

urlpatterns = [
    path('books_list/', BooksList.as_view(), name='books_list'),
    path('about_us/', about_us, name='about_us'),
]