from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.boards, name="boards"),
    path('manage_board', views.manage_board, name="manage_board"),
    path('update_board/<str:pk>', views.update_board, name="update_board"),
    path('delete_board/<str:pk>', views.delete_board, name="delete_board"),
    path('manage_super_users/<str:pk>',
         views.manage_superusers, name="manage_superusers"),

    path('boards/', views.boards, name="boards"),
    path('boards/<str:pk>', views.boards, name="boards"),
    # path('get_board/<str:pk>', views.get_board, name="get_board"),
    path('create_board/', views.create_board, name="create_board"),
    path('boards/claim_ticket/<str:pk>',
         views.claim_ticket, name="claim_ticket"),

]
