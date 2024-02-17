from django.urls import path
from . import views

urlpatterns = [
    path('playlist/', views.find_playlist, name='find_playlist'),
    path('add', views.add_to_playlist, name='add_to_playlist'),
]