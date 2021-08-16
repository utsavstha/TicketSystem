from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('home.urls')),
    path('', include('group.urls')),
    path('', include('classification.urls')),
    path('', include('priority.urls')),
    path('', include('ticket.urls')),
    path('', include('board.urls')),
    path('', include('email_setting.urls')),

]
