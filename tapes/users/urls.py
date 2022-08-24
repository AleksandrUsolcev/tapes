from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path, re_path

from . import views

app_name = 'users'

urlpatterns = [
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logout.html'),
        name='logout'
    ),
    path('signup-modal/',
         views.SignUpView.as_view(),
         name='signup_modal'),
    path(
        'login-modal/',
        views.CustomLoginView.as_view(),
        name='login_modal'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(
            template_name='users/password_reset_form.html'),
        name='password_reset_form'
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='users/password_change_done.html'),
        name='password_reset_complete'
    ),
    path(
        'password_change/',
        PasswordChangeView.as_view(
            template_name='users/password_change_form.html'),
        name='password_change_form'
    ),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'),
        name='password_change_done'
    ),
    re_path(r'^~(?P<username>\w+)/$',
            views.UserProfileView.as_view(),
            name='profile'
            ),
    path('edit-profile/',
         views.UserEditView.as_view(),
         name='user_edit'),
    path(
        '~<slug:username>/subscribe',
        views.SubscribeView.as_view(),
        name='subscribe'
    ),
]
