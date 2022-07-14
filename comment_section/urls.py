from django.urls import path
from .views import comment, comment_ist

app_name = 'comment_section'

urlpatterns = [
    path('comment/<slug:slug>', comment, name='comment'),
    path('comment_list/<slug:slug>/', comment_ist, name='comment_ist'),
]