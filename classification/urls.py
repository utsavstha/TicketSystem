from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('classification/', views.classification, name="classification"),
    path('create_classification/', views.create_classification,
         name="create_classification"),
    path('update_classification/<str:pk>',
         views.update_classification, name="update_classification"),
    path('delete_classification/<str:pk>',
         views.delete_classification, name="delete_classification"),

]
