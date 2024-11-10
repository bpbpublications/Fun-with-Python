"""chatter URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from chat.views import main_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('', main_view, name='main_view'),
]
