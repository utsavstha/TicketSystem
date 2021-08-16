from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('email_settings/', views.email_settings, name="email_settings"),
    path('create_email_settings/', views.create_email_settings,
         name="create_email_settings"),
    path('update_email_settings/<str:pk>',
         views.update_email_settings, name="update_email_settings"),

]
