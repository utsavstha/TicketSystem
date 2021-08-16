from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('groups/', views.groups, name="groups"),
    path('create_group/', views.create_group, name="create_group"),
    # path('logout/', views.logout_request, name="logout"),
    # path('users/', views.users, name="users"),
    # path('create_user/', views.create_user, name="create_user"),
    path('update_group/<str:pk>', views.update_group, name="update_group"),
    path('delete_group/<str:pk>', views.delete_group, name="delete_group"),

]
