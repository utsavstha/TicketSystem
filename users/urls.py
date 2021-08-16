from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_request, name="login"),
    path('register/', views.register_request, name="register"),
    path('logout/', views.logout_request, name="logout"),
    path('users/', views.users, name="users"),
    path('create_user/', views.create_user, name="create_user"),
    path('update_user/<str:pk>', views.update_user, name="update_user"),
    path('delete_user/<str:pk>', views.delete_user, name="delete_user"),
    path('change_password/<str:pk>',
         views.change_password, name="change_password"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_sent.html'),
        name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_done.html'), name="password_reset_complete"),
]
