from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = 'api'

urlpatterns = [
    path('books_list/', views.books_list, name='books_list'),
    path('books_detail/<int:pk>/', views.BookDetailView.as_view(), name='books_detail'),
    path('new_publish_book/', views.NewPublishBookView.as_view(), name='new_publish_book'),
    path('best_seller_book/', views.BestSellerBookView.as_view(), name='best_seller_book'),
    path('authors_list/', views.authors_list, name='authors_list'),
    path('categories_list/', views.BookCategoryView.as_view(), name='categories_list'),
    path('publisher_list/', views.BookPublisherView.as_view(), name='publisher_list'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('comment/', views.CommentView.as_view(), name='comment'),
    path('profile/<int:pk>', views.UserProfileView.as_view(), name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]