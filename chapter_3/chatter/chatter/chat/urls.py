from django.urls import path

from . import views

urlpatterns = [
    path('query', views.chat_query, name='chat_query'),
]