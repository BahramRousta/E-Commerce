from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import ResetPasswordRequestEmail

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

    path('add_to_favorite/', views.FavoriteBookView.as_view(), name='add_to_favorite'),
    path('delete_from_favorite/<int:pk>/', views.FavoriteBookView.as_view(), name='delete_from_favorite'),

    path('cart_item/', views.CartItemView.as_view(), name='cart_item'),
    path('cart_item_update/<int:pk>/', views.CartItemView.as_view(), name='cart_item_update'),
    path('delete_cart_item/<int:pk>/', views.CartItemView.as_view(), name='delete_cart_item'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogOut.as_view(), name='logout'),
    path('change_password/<int:pk>/', views.ChangePasswordView.as_view(), name='change_password'),
    path('request-reset-email/', ResetPasswordRequestEmail.as_view(), name="request-reset-email"),
    path('profile/<int:pk>', views.UserProfileView.as_view(), name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]