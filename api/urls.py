from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token
app_name = 'api'

urlpatterns = [
    path('books_list/', views.books_list, name='books_list'),
    path('books_detail/<str:slug>/', views.BookDetailView.as_view(), name='books_detail'),
    path('new_publish_book/', views.NewPublishBookView.as_view(), name='new_publish_book'),
    path('best_seller_book/', views.BestSellerBookView.as_view(), name='best_seller_book'),
    path('authors_list/', views.authors_list, name='authors_list'),
    path('categories_list/', views.BookCategoryView.as_view(), name='categories_list'),
    path('publisher_list/', views.BookPublisherView.as_view(), name='publisher_list'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('comment/', views.CommentView.as_view(), name='comment'),
    path('user_profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('user_register/', views.register, name='user_register'),
    path('login/', obtain_auth_token, name='login'),
]