from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView, LoginView, profile, LogOutView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('log_out/', LogOutView.as_view(), name='log_out'),
    path('profile/', profile, name='profile'),

    # Use django auth_views
    # change password urls

    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='accounts/change-password.html'),
         name='password_change'),

    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),

    # reset password urls

    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),


    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
]
