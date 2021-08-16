from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('priorities/', views.priorities, name="priorities"),
    path('create_priority/', views.create_priority,
         name="create_priority"),
    path('update_priority/<str:pk>',
         views.update_priority, name="update_priority"),
    path('delete_priority/<str:pk>',
         views.delete_priority, name="delete_priority"),

]
