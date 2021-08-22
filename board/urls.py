from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.boards, name="boards"),
    path('boards/', views.boards, name="boards"),
    path('boards/<str:pk>', views.boards, name="boards"),
    # path('get_board/<str:pk>', views.get_board, name="get_board"),
    path('create_board/', views.create_board, name="create_board"),
    path('boards/claim_ticket/<str:pk>',
         views.claim_ticket, name="claim_ticket"),

]
