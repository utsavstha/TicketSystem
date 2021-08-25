from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('tickets/', views.tickets, name="tickets"),
    path('ticket_info/<str:pk>', views.ticket_info, name="ticket_info"),
    path('boards/change_ticket_state/', views.change_state,
         name="change_ticket_state"),
    path('change_ticket_state/', views.change_state,
         name="change_ticket_state"),
    path('get_board/change_ticket_state/', views.change_state,
         name="change_ticket_state"),

    path('ticket_logs/<str:pk>', views.view_logs, name="ticket_logs"),
    path('quick_attach/<str:pk>', views.quick_attach, name="quick_attach"),
    path('post_comment/<str:pk>', views.post_comment, name="post_comment"),

    path('create_ticket/', views.create_ticket,
         name="create_ticket"),
    path('update_ticket/<str:pk>',
         views.update_ticket, name="update_ticket"),
    path('delete_ticket/<str:pk>',
         views.delete_ticket, name="delete_ticket"),
    path('delete_attachment/<str:pk>',
         views.delete_attachment, name="delete_attachment"),

]
